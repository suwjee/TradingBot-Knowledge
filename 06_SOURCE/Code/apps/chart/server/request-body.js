import { StringDecoder } from "node:string_decoder";

export function readBoundedBody(req, maxBytes, tooLargeMessage = "Request is too large") {
  if (!Number.isSafeInteger(maxBytes) || maxBytes < 0) {
    throw new Error("Request body limit must be a non-negative integer.");
  }

  return new Promise((resolve, reject) => {
    let body = "";
    let bytes = 0;
    let settled = false;
    const decoder = new StringDecoder("utf8");

    const cleanup = () => {
      req.off("data", onData);
      req.off("end", onEnd);
      req.off("error", onError);
      req.off("aborted", onAborted);
      req.off("close", onClose);
    };
    const finish = (error) => {
      if (settled) return;
      settled = true;
      cleanup();
      if (error) reject(error);
      else resolve(body);
    };
    const drainRejected = () => {
      const ignoreDrainError = () => {};
      const stopDraining = () => {
        req.off("end", stopDraining);
        req.off("error", ignoreDrainError);
        req.off("aborted", stopDraining);
        req.off("close", stopDraining);
      };
      req.once("end", stopDraining);
      req.on("error", ignoreDrainError);
      req.once("aborted", stopDraining);
      req.once("close", stopDraining);
      req.resume();
    };
    const onData = (part) => {
      const chunk = Buffer.isBuffer(part) ? part : Buffer.from(part);
      bytes += chunk.length;
      if (bytes > maxBytes) {
        body = "";
        finish(new Error(tooLargeMessage));
        drainRejected();
        return;
      }
      body += decoder.write(chunk);
    };
    const onEnd = () => { body += decoder.end(); finish(); };
    const onError = (error) => { finish(error); drainRejected(); };
    const onAborted = () => { finish(new Error("Request was aborted.")); drainRejected(); };
    const onClose = () => finish(new Error("Request was aborted."));

    req.on("data", onData);
    req.once("end", onEnd);
    req.once("error", onError);
    req.once("aborted", onAborted);
    req.once("close", onClose);
  });
}
