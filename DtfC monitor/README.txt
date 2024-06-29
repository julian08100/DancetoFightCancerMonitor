Sure! Below is a GitHub README text that explains how to use the provided HTML files and scripts. This guide assumes the URLs have been removed and users will need to insert their own URLs where necessary.

---

# Dance to Fight Cancer Web Pages

This repository contains HTML files and scripts for the Dance to Fight Cancer fundraising event. These pages display the amount raised by different teams and the top donors.

## Files Included

- `home.html`
- `donateur.html`
- `nieuwe donateurs.html`
- `topdonateurs.html`
- `totale opbrengst.html`

## Usage

### Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/your-username/dance-to-fight-cancer.git
cd dance-to-fight-cancer
```

### Step 2: Insert Your URLs

Replace the placeholder URLs in the HTML files with your own URLs where data is fetched. Look for the `fetch` function in each file and update the URL accordingly.

Example:
```html
<script>
    function fetchData() {
        fetch('YOUR_URL_HERE')
            .then(response => response.text())
            .then(data => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(data, 'text/html');
                
                const lionsAmountElement = doc.querySelector('div.wp-block-column:nth-child(1) p.has-huge-font-size strong');
                const studsAmountElement = doc.querySelector('div.wp-block-column:nth-child(2) p.has-huge-font-size strong');

                const lionsAmount = lionsAmountElement ? lionsAmountElement.textContent : "€0";
                const studsAmount = studsAmountElement ? studsAmountElement.textContent : "€0";

                updateAmount('lions-amount', lionsAmount);
                updateAmount('studs-amount', studsAmount);
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    function updateAmount(elementId, newAmount) {
        const element = document.getElementById(elementId);
        if (element && element.textContent !== newAmount) {
            element.textContent = newAmount;
            element.classList.add('updated');
            setTimeout(() => element.classList.remove('updated'), 1000);
        }
    }

    setInterval(fetchData, 1000);
    fetchData();  // Initial fetch to set the values
</script>
```

### Step 3: Serve the HTML Files

You can serve the HTML files using a simple HTTP server. If you have Python installed, you can use the following command in the directory containing your HTML files:

```bash
python -m http.server
```

This will start a local server at `http://localhost:8000`. Open this URL in your browser to view the pages.

### Step 4: Customize the Styles

Each HTML file contains inline styles for customizing the appearance of the pages. You can modify these styles to fit your needs.

Example:
```html
<style>
    .amount {
        font-size: 6em;
        color: #FFA500;
        transition: all 0.5s ease-in-out;
        font-weight: bold;
        margin-bottom: -10px;
        text-align: center;
    }
    .updated {
        color: #32CD32;
        transform: scale(1.2);
    }
</style>
```

### Step 5: Update Content

Update the static content within the HTML files to reflect the current status of your fundraising event. This includes text, images, and other elements.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README as needed for your specific project requirements. If you have any additional questions or need further assistance, let me know!