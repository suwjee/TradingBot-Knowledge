import fs from "node:fs";
import { createHash } from "node:crypto";

const identityFields = ["dev", "ino", "size", "birthtimeMs", "ctimeMs", "mtimeMs"];
const changedMessage = "The selected RAW file changed while calculating. Apply again with the current file.";

function sameStat(left, right) {
  return left.isFile() && right.isFile()
    && identityFields.every((field) => left[field] === right[field]);
}

export async function captureRawInputIdentity(sourcePath) {
  try {
    const before = fs.statSync(sourcePath);
    if (!before.isFile()) throw new Error(changedMessage);
    const hash = createHash("sha256");
    for await (const chunk of fs.createReadStream(sourcePath)) hash.update(chunk);
    const after = fs.statSync(sourcePath);
    if (!sameStat(before, after)) throw new Error(changedMessage);
    return { stat: after, sha256: hash.digest("hex") };
  } catch {
    throw new Error(changedMessage);
  }
}

export async function assertRawInputUnchanged(sourcePath, selected) {
  const current = await captureRawInputIdentity(sourcePath);
  if (!sameStat(current.stat, selected.stat) || current.sha256 !== selected.sha256) {
    throw new Error(changedMessage);
  }
}
