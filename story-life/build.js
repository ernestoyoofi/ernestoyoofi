const fs = require("fs")

const mainstorylife = "./main.md"
const jsonlisttop = "./result/top.json"
const jsonlistall = "./result/all.json"

function parseTextContent(content) {
  const blocks = content.split(/---/);
  const results = [];

  blocks.forEach(block => {
    if (!block.includes('> "')) return;

    const quoteMatch = block.match(/> "([^"]+)"\s*\n>\s*EN:\s*"([^"]+)"/);
    const categoryMatch = block.match(/- \*\*Category:\*\*\s*([^\n]+)/);
    const meanEnMatch = block.match(/- en\s*:\s*`([\s\S]*?)`/);
    const meanIdMatch = block.match(/- id\s*:\s*`([\s\S]*?)`/);
    if (quoteMatch) {
      results.push({
        quoted: {
          id: quoteMatch[1].trim(),
          en: quoteMatch[2].trim()
        },
        mean: {
          en: meanEnMatch ? meanEnMatch[1].trim() : "",
          id: meanIdMatch ? meanIdMatch[1].trim() : ""
        },
        category: categoryMatch ? categoryMatch[1].trim() : "Unknown"
      });
    }
  });
  return results;
}

const readfile = fs.readFileSync(mainstorylife, "utf-8")
const parse = parseTextContent(readfile)

fs.writeFileSync(jsonlistall, JSON.stringify(parse, null, 2))
fs.writeFileSync(jsonlisttop, JSON.stringify(parse.slice(0, 30), null, 2))