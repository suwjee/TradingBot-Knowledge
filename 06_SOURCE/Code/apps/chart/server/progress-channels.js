const HISTORY_LIMIT = 120;

export function createProgressChannels() {
  const channels = new Map();
  let closed = false;

  function get(id) {
    let channel = channels.get(id);
    if (!channel) {
      channel = { events: [], clients: new Set() };
      channels.set(id, channel);
    }
    return channel;
  }

  function releaseIfObserved(id, channel) {
    if (channel.clients.size || channels.get(id) !== channel) return;
    if (!channel.events.length || channel.events.at(-1)?.status === "finished") channels.delete(id);
  }

  function publish(id, event) {
    if (!id || closed) return;
    const channel = get(id);
    channel.events.push(event);
    if (channel.events.length > HISTORY_LIMIT) channel.events.shift();
    const message = `data: ${JSON.stringify(event)}\n\n`;
    for (const client of channel.clients) {
      try { client.write(message); }
      catch { channel.clients.delete(client); }
    }
  }

  function attach(id, client) {
    if (closed) { client.end(); return () => {}; }
    const channel = get(id);
    channel.clients.add(client);
    for (const event of channel.events) {
      try { client.write(`data: ${JSON.stringify(event)}\n\n`); }
      catch { channel.clients.delete(client); break; }
    }
    return () => {
      channel.clients.delete(client);
      releaseIfObserved(id, channel);
    };
  }

  function close() {
    if (closed) return;
    closed = true;
    for (const channel of channels.values()) {
      for (const client of channel.clients) {
        try { client.end(); } catch { /* A disconnected response cannot block shutdown. */ }
      }
      channel.clients.clear();
    }
    channels.clear();
  }

  function stats() {
    let clients = 0;
    for (const channel of channels.values()) clients += channel.clients.size;
    return { channels: channels.size, clients };
  }

  return { publish, attach, close, stats };
}
