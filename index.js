const fs = require('fs');
const csv = require('csv-parser');
const chokidar = require('chokidar');

const csvFilePath = 'accounts.csv';  // Path to your CSV file
const mdFilePath = 'table.md';       // Path to the output Markdown file

const csvToMarkdown = (csvFilePath, mdFilePath) => {
    const headers = [];
    const rows = [];

    fs.createReadStream(csvFilePath)
        .pipe(csv())
        .on('headers', (headerList) => {
            headers.push(...headerList);
        })
        .on('data', (row) => {
            rows.push(row);
        })
        .on('end', () => {
            // Calculate the maximum width for each column
            const maxWidths = headers.map(header => Math.max(header.length, ...rows.map(row => (row[header] || '').length)));

            // Function to pad each cell content to align with the column width
            const padCell = (text, width) => text.padEnd(width);

            // Create Markdown table with aligned columns
            let markdown = `| ${headers.map((header, i) => padCell(header, maxWidths[i])).join(' | ')} |\n`;
            markdown += `| ${maxWidths.map(width => '-'.repeat(width)).join(' | ')} |\n`;

            rows.forEach(row => {
                markdown += `| ${headers.map((header, i) => padCell(row[header] || '', maxWidths[i])).join(' | ')} |\n`;
            });

            fs.writeFileSync(mdFilePath, markdown, 'utf8');
            console.log('Markdown file updated.');
        });
};

const watchFile = (filePath) => {
    chokidar.watch(filePath, { persistent: true })
        .on('change', () => {
            console.log(`${filePath} has been changed. Updating Markdown file...`);
            csvToMarkdown(csvFilePath, mdFilePath);
        });
};

// Initial conversion
csvToMarkdown(csvFilePath, mdFilePath);

// Watch for file changes
watchFile(csvFilePath);

