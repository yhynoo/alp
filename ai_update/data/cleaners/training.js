import data from '../4ky_clean.json' with { type: 'json' }
import { cleanTranscription } from './cleaner.js'

const filteredData = [];
const accountTypeCounts = {}; // Track counts for each accountType

data.forEach((_item) => {
    let item = _item;

    // Filtering after adjustments
    if (item.inscription.accountType.includes("economic") && item.inscription.accountType.length > 1) {
       // Clean accountType: remove parenthesis content
        const cleanedAccountTypes = item.inscription.accountType
            .map(type => type.replace(/\s*\(.*?\)\s*/g, '').trim()) // Remove text inside parentheses
            .filter(type => type !== "economic"); // Remove "economic" after cleaning

        // Check if the transcription has at least 6 words
        if (item.inscription.transliterationClean.split(/\s+/).filter(word => word.length > 0).length >= 6) {
            const filteredItem = {
                designation: item.designation,
                link: item.link,
                accountType: cleanedAccountTypes,

                withoutNumbers: cleanTranscription(item.inscription.transliterationClean)
                    .split('\n') // Split into lines
                    .map(line => line
                        .replace(/\b\d+N\d+\d+(?:~[A-Za-z])?\b/g, '')
                        .replace(/ {2,}/g, ' ')
                        .trim()
                    )
                    .join('\n'), // Merge back into a string

                withNumbers: cleanTranscription(item.inscription.transliterationClean)
                    .replace(/\b(\d+)(N)/g, '$2')
            };

            // Count each cleaned accountType
            cleanedAccountTypes.forEach(type => {
                accountTypeCounts[type] = (accountTypeCounts[type] || 0) + 1;
            });

            filteredData.push(filteredItem);
        }
    }
});

// Save the filtered training data
await Deno.writeTextFile('data/trainingData.json', JSON.stringify(filteredData, null, 4));

// Generate the report
const reportLines = ["Input Account Types:\n"];
Object.entries(accountTypeCounts).forEach(([type, count]) => {
    reportLines.push(`${type}: ${count} records`);
});

// Save the report
await Deno.writeTextFile('reports/account_type_report.txt', reportLines.join("\n"));

console.log(`Filtering complete. ${filteredData.length} items found.`);
console.log("Account type report saved to 'reports/account_type_report.txt'.");
