const fs = require("fs")

const mainstorylife = "./main.md"
const jsonlisttop = "./result/top.json"
const jsonlistall = "./result/all.json"

function parseStoryLife(content) {
  const blocks = content.split('---');
  const results = [];

  blocks.forEach(block => {
    const lines = block.split('\n').map(line => line.trim());
    
    // Cari kutipan (baris yang mulai dengan >)
    const quotes = lines
      .filter(l => l.startsWith('>'))
      .map(l => {
        const match = l.match(/"([^"]+)"/);
        return match ? match[1] : null;
      })
      .filter(Boolean);

    if (quotes.length === 0) return; // Skip jika bukan blok kutipan

    // Cari Category
    const categoryLine = lines.find(l => l.includes('**Category:**'));
    const category = categoryLine ? categoryLine.split('**Category:**')[1].trim() : "Unknown";

    // Cari Mean (Mengambil teks di antara backtick)
    const findMean = (lang) => {
      const line = lines.find(l => l.toLowerCase().startsWith(`- ${lang.toLowerCase()} :`));
      if (!line) return "";
      const match = line.match(/`([\s\S]*?)`/);
      return match ? match[1] : "";
    };

    results.push({
      quoted: {
        id: quotes[0] || "",
        en: quotes[1] || ""
      },
      mean: {
        id: findMean('id'),
        en: findMean('en'),
      },
      category: category
    });
  });

  return results;
}

const readfile = fs.readFileSync(mainstorylife, "utf-8")
const parse = parseStoryLife(readfile)

fs.writeFileSync(jsonlistall, JSON.stringify(parse, null, 2))
fs.writeFileSync(jsonlisttop, JSON.stringify(parse.slice(0, 30), null, 2))