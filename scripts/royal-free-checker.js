const { chromium } = require("playwright");

const targets = [
  {
    name: "Royal Free Nursing/Midwifery",
    url: "https://www.royalfree.nhs.uk/working-here/our-current-vacancies#!/job_list/s1/Nursing_Midwifery?_ts=1",
    required: [/band 3/i, /bank/i, /healthcare|health care|hca|assistant/i],
  },
  {
    name: "Royal Free Administrative Services",
    url: "https://www.royalfree.nhs.uk/working-here/our-current-vacancies#!/job_list/s7/Administrative_Services?_ts=1",
    required: [/band 3/i, /bank/i, /admin|clerical|assistant|reception|coordinator/i],
  },
];

function normalize(text) {
  return text.replace(/\s+/g, " ").trim();
}

async function extractJobs(page) {
  return page.evaluate(() => {
    return [...document.querySelectorAll("a")]
      .map((anchor) => {
        const text = (anchor.innerText || anchor.textContent || "").replace(/\s+/g, " ").trim();
        const parent = (anchor.closest("li, article, .job, .vacancy, .nhsuk-card, div")?.innerText || "")
          .replace(/\s+/g, " ")
          .trim();
        return {
          text: parent || text,
          href: anchor.href,
        };
      })
      .filter((job) => /band|bank|assistant|clerical|healthcare|admin|nurse|midwifery/i.test(job.text))
      .filter((job, index, all) => all.findIndex((other) => other.href === job.href) === index);
  });
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1365, height: 900 } });
  const results = [];

  for (const target of targets) {
    await page.goto(target.url, { waitUntil: "networkidle", timeout: 60000 });
    await page.waitForTimeout(5000);
    const jobs = await extractJobs(page);
    const exactMatches = jobs.filter((job) => target.required.every((rule) => rule.test(job.text)));
    const band3Related = jobs.filter((job) => /band 3/i.test(job.text));

    results.push({
      target: target.name,
      checkedAt: new Date().toISOString(),
      exactMatches: exactMatches.map((job) => ({ ...job, text: normalize(job.text) })),
      band3Related: band3Related.map((job) => ({ ...job, text: normalize(job.text) })),
    });
  }

  await browser.close();
  console.log(JSON.stringify(results, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
