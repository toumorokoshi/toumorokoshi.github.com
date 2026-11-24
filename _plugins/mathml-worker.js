"use strict";

const readline = require("readline");
const temml = require("temml");

const rl = readline.createInterface({
  input: process.stdin,
  crlfDelay: Infinity,
});

rl.on("line", (line) => {
  if (!line.trim()) {
    return;
  }

  try {
    const { tex, displayMode } = JSON.parse(line);
    const html = temml.renderToString(tex, {
      displayMode: Boolean(displayMode),
      throwOnError: false,
    });
    process.stdout.write(JSON.stringify({ html }) + "\n");
  } catch (err) {
    process.stdout.write(JSON.stringify({ error: err.message }) + "\n");
  }
});
