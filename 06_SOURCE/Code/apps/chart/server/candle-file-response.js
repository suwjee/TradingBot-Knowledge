import fs from "node:fs";

function entityTag(stat) {
  return `"${Number(stat.size).toString(16)}-${Math.trunc(Number(stat.mtimeMs)).toString(16)}"`;
}

function matchesEntityTag(header, expected) {
  return String(header || "")
    .split(",")
    .map((value) => value.trim().replace(/^W\//, ""))
    .includes(expected);
}

export function sendCandleFile(req, res, dataPath) {
  return new Promise((resolve, reject) => {
    const stat = fs.statSync(dataPath);
    const etag = entityTag(stat);
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.setHeader("Cache-Control", "private, no-cache");
    res.setHeader("ETag", etag);
    res.setHeader("Content-Length", stat.size);
    if (matchesEntityTag(req.headers?.["if-none-match"], etag)) {
      res.statusCode = 304;
      res.removeHeader?.("Content-Length");
      res.end();
      resolve();
      return;
    }
    const stream = fs.createReadStream(dataPath);
    stream.on("error", reject);
    res.on("finish", resolve);
    res.on("error", reject);
    stream.pipe(res);
  });
}
