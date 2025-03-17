import data from '../4ky_clean.json' with {type: 'json'}
import { cleanTranscription } from './cleaner.js'
const filteredData = [];

data.forEach((_item) => {
    let item = _item

    // adjustments: remove fruits, textiles and dairy texts
    item.inscription.accountType = item.inscription.accountType.filter(
        (type) => type !== "fruits" && type !== "textiles" && type !== "dairy"
    );

    // filtering after adjustments
    if (item.inscription.accountType.includes("economic") && item.inscription.accountType.length === 1) {
        const filteredItem = {
            designation: item.designation,
            link: item.link,
            accountType: item.inscription.accountType,

            withNumbers: cleanTranscription(item.inscription.transliterationClean)
        };

    filteredData.push(filteredItem);
    }
});

Deno.writeTextFile('data/corpusClean.json', JSON.stringify(filteredData, null, 4))
console.log(`Filtering complete. ${filteredData.length} items found.`);
