import path from "node:path";
import { fileURLToPath } from "node:url";


const pluginRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const skillsDirectory = path.join(pluginRoot, "skills");

const commands = {
  brainstorm: "Develop one initiative into a dated, approved specification without implementing it.",
  plan: "Derive a test-first implementation plan from an approved JSIP specification.",
  implement: "Execute an approved JSIP plan test-first with strict intent-drift controls.",
};


export const JsipPlugin = async () => ({
  config: async (config) => {
    config.skills ??= {};
    config.skills.paths ??= [];
    if (!config.skills.paths.includes(skillsDirectory)) {
      config.skills.paths.push(skillsDirectory);
    }

    config.command ??= {};
    for (const [skill, description] of Object.entries(commands)) {
      const name = `jsip:${skill}`;
      config.command[name] ??= {
        description,
        template: [
          `This is an explicit ${name} invocation.`,
          `Use OpenCode's native skill tool to load \`${skill}\`, then follow that skill exactly.`,
          "Do not substitute another workflow or automatically continue to a later JSIP stage.",
          "User arguments: $ARGUMENTS",
        ].join("\n"),
      };
    }
  },
});
