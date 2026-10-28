const MAX_ENGINE_CONCURRENCY = 8;
const PROGRESS_HISTORY_LIMIT = 120;

export function parseEngineConcurrency(value) {
  if (value === undefined) return 1;
  if (typeof value !== "string" || !/^[1-8]$/.test(value)) {
    throw new Error(`TRADINGBOT_MAX_ENGINE_CONCURRENCY must be an integer from 1 to ${MAX_ENGINE_CONCURRENCY}.`);
  }
  return Number(value);
}

export function createCalculationCoordinator({ maxActive = 1 } = {}) {
  if (!Number.isInteger(maxActive) || maxActive < 1 || maxActive > MAX_ENGINE_CONCURRENCY) {
    throw new Error(`Engine concurrency must be an integer from 1 to ${MAX_ENGINE_CONCURRENCY}.`);
  }

  const pending = [];
  const inFlight = new Map();
  const activeJobs = new Set();
  let closed = false;

  function publish(job, event) {
    job.events.push(event);
    if (job.events.length > PROGRESS_HISTORY_LIMIT) job.events.shift();
    for (const subscriber of job.subscribers) {
      try { subscriber(event); }
      catch { job.subscribers.delete(subscriber); }
    }
  }

  function subscribe(job, onProgress) {
    if (typeof onProgress !== "function") return;
    job.subscribers.add(onProgress);
    for (const event of job.events) {
      try { onProgress(event); }
      catch { job.subscribers.delete(onProgress); break; }
    }
  }

  function drain() {
    if (closed) return;
    while (activeJobs.size < maxActive && pending.length) {
      const job = pending.shift();
      const controller = new AbortController();
      job.controller = controller;
      activeJobs.add(job);
      let result;
      try { result = job.execute((event) => publish(job, event), controller.signal); }
      catch (error) { result = Promise.reject(error); }
      Promise.resolve(result).then(
        (value) => settle(job, true, value),
        (error) => settle(job, false, error),
      );
    }
  }

  function settle(job, succeeded, value) {
    activeJobs.delete(job);
    inFlight.delete(job.key);
    job.subscribers.clear();
    job.events.length = 0;
    if (!succeeded) job.reject(value);
    else job.resolve(value);
    drain();
  }

  function run(key, execute, onProgress) {
    if (closed) return Promise.reject(new Error("Server is shutting down."));
    const existing = inFlight.get(key);
    if (existing) {
      subscribe(existing, onProgress);
      return existing.promise;
    }
    let resolve;
    let reject;
    const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
    const job = { key, execute, resolve, reject, promise, subscribers: new Set(), events: [], controller: null };
    subscribe(job, onProgress);
    inFlight.set(key, job);
    pending.push(job);
    drain();
    return promise;
  }

  function close() {
    if (closed) return;
    closed = true;
    for (const job of pending.splice(0)) {
      inFlight.delete(job.key);
      job.subscribers.clear();
      job.events.length = 0;
      job.reject(new Error("Server is shutting down."));
    }
    for (const job of activeJobs) job.controller.abort();
  }

  function stats() {
    return { active: activeJobs.size, pending: pending.length, inFlight: inFlight.size };
  }

  return { run, close, stats };
}
