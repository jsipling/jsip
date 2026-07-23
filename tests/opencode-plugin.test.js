import assert from "node:assert/strict";
import test from "node:test";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { JsipPlugin } from "../.opencode/plugins/jsip.js";


const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");


test("registers the shared skills directory and namespaced commands", async () => {
  const hooks = await JsipPlugin({});
  const config = {};

  await hooks.config(config);

  assert.deepEqual(config.skills.paths, [path.join(root, "skills")]);
  for (const skill of ["brainstorm", "plan", "implement"]) {
    const command = config.command[`jsip:${skill}`];
    assert.ok(command, `missing jsip:${skill}`);
    assert.match(command.template, new RegExp(`load.*${skill}`, "i"));
    assert.match(command.template, /\$ARGUMENTS/);
  }
});


test("does not duplicate paths or replace existing commands", async () => {
  const hooks = await JsipPlugin({});
  const existing = { template: "keep me" };
  const config = {
    skills: { paths: [path.join(root, "skills")] },
    command: { "jsip:plan": existing },
  };

  await hooks.config(config);
  await hooks.config(config);

  assert.deepEqual(config.skills.paths, [path.join(root, "skills")]);
  assert.equal(config.command["jsip:plan"], existing);
  assert.ok(config.command["jsip:brainstorm"]);
  assert.ok(config.command["jsip:implement"]);
});
