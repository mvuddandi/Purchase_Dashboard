from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Function to generate data for the line plot
def get_plot_data():
    # Load your CSV data
    df = pd.read_csv('purchasehistory.csv')

    # Convert 'year_month' column to datetime and sort
    df['year_month'] = pd.to_datetime(df['year_month'], format='%Y-%m')
    df = df.sort_values(by=['year_month'])

    # Group the data by 'year_month'
    grouped_data = df.groupby('year_month').sum()

    # Prepare the data to send to the frontend
    data = {
        "labels": grouped_data.index.strftime('%b %Y').tolist(),  # Convert datetime to 'Jan 2021', 'Feb 2021', etc.
        "purchase_request_value": grouped_data['purchase_request_value'].tolist(),
        "po_value": grouped_data['po_value'].tolist(),
        "inventory_receipt_value": grouped_data['inventory_receipt_value'].tolist(),
        "invoiced_value": grouped_data['invoiced_value'].tolist()
    }

    return data

def get_boxplot_data():
    # Load your CSV data
    mat_prices = pd.read_csv('Mat_Rates.csv')

    # Prepare the data for the box plot
    data = {
        "materials": mat_prices['Material'].tolist(),
        "prices": mat_prices['Price'].tolist()
    }

    return data

def get_histogram_data():
    # Load your CSV data
    item_group = pd.read_csv('item-group.csv')

    # Group by 'Item Group' and sum the 'Inventory Value'
    ig_grouped = item_group.groupby('Item Group')['Inventory Value'].sum().reset_index()

    # Convert Inventory Value to Lakhs
    ig_grouped['Inventory Value'] = ig_grouped['Inventory Value'] / 100000

    # Prepare the data to send to the frontend
    data = {
        "item_groups": ig_grouped['Item Group'].tolist(),
        "inventory_values": ig_grouped['Inventory Value'].tolist()
    }

    return data

def get_scatter_data():
    # Load your CSV data (assuming 'purchase_data' is your data source)
    purchase_data = pd.read_csv('purchasehistory.csv')

    # Prepare the data to send to the frontend
    data = {
        "purchase_request_value": purchase_data['purchase_request_value'].tolist(),
        "po_value": purchase_data['po_value'].tolist()
    }

    return data


def get_stacked_bar_data():
  
    new_doc_status = pd.read_csv('doc_status.csv')


    pivot_data = new_doc_status.pivot(index='Document', columns='Status', values='Count').fillna(0)


    data = {
        "document_types": pivot_data.index.tolist(),
        "statuses": pivot_data.columns.tolist(),
        "values": pivot_data.values.tolist()  
    }

    return data

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/line-plot-data')
def line_plot_data():
    data = get_plot_data()
    return jsonify(data)

@app.route('/boxplot-data')
def boxplot_data():
    data = get_boxplot_data()
    return jsonify(data)

@app.route('/histogram-data')
def histogram_data():
    data = get_histogram_data()
    return jsonify(data)

@app.route('/scatterplot-data')
def scatterplot_data():
    data = get_scatter_data()
    return jsonify(data)

@app.route('/stacked-bar-data')
def stacked_bar_data():
    data = get_stacked_bar_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)
