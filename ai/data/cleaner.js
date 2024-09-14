import data from './4ky_source.json' with {type: 'json'}
const filteredData = [];

data.forEach((_item) => {
    let item = _item

    // adjustments: remove fruits, textiles and dairy texts
    item.inscription.accountType = item.inscription.accountType.filter(
        (type) => type !== "fruits" && type !== "textiles" && type !== "dairy"
    );

    // filtering after adjustments
    if (item.inscription.accountType.includes("economic") && item.inscription.accountType.length > 1) {
        const filteredItem = {
            designation: item.designation,
            accountType: item.inscription.accountType.filter(
                (type) => type !== "economic"
            ),
            withoutNumbers: item.ai.transcriptionCasesNoNumbers
                .replace(/~[a-z](\d)?/g, ''),

            withNumbers: item.ai.transcriptionCasesNumbers
                .replace(/\b(\d+)(N)/g, '$2')
                .replace(/~[a-z](\d)?/g, '')
        };

    filteredData.push(filteredItem);
    }
});

Deno.writeTextFile('ai/data/aiInput.json', JSON.stringify(filteredData, null, 4))
console.log(`Filtering complete. ${filteredData.length} items found.`);
