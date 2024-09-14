import data from './aiInput.json' with {type: 'json'}

// Initialize counters
let accountTypeCounts = {};
let multiAccountTypeCount = 0;

data.forEach(item => {
    // Check if the item has more than one accountType
    if (item.accountType.length > 1) {
        multiAccountTypeCount++;
    } else {
        // Count the occurrences of each accountType
        item.accountType.forEach(type => {
            if (accountTypeCounts[type]) {
                accountTypeCounts[type]++;
            } else {
                accountTypeCounts[type] = 1;
            }
        });
    }    
});

// Output the results
console.log("Account Type Counts:", accountTypeCounts);
console.log("Number of texts with more than one account type:", multiAccountTypeCount);
