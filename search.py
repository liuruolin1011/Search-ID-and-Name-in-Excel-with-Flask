from flask import Flask, request, render_template, Blueprint
import pandas as pd

app = Flask(__name__)

escalated_alerts = pd.read_excel('Escalated alerts August 2024.xlsx')
hrj = pd.read_excel('HRJ_20230901-20240831.xlsx')

def search_in_files(search_term, search_type, file_choice):
    if file_choice == 'escalated_alerts':
        if search_type == 'ID':
            result = escalated_alerts[escalated_alerts['Key Identifiers (account / ID)'].astype(str).str.contains(str(search_term), na=False)]
        else:
            result = escalated_alerts[escalated_alerts['Name of Subject (could be victim; some are denoted)'].astype(str).str.contains(search_term, case=False, na=False)]
        
        if not result.empty:
            return result.to_html(classes='table table-striped')
        else:
            return f'No match found for {search_term} in escalated alerts list'
    
    # search in HRJ
    elif file_choice == 'hrj':
        result = hrj[hrj['CIF'].astype(str).str.contains(str(search_term))]
        if not result.empty:
            value_in_col_B = result.iloc[0, 1]
            return f'For ID {search_term}, the HRJ search result is {value_in_col_B}'
        else:
            return f'No match found for ID {search_term} in HRJ list'

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        search_type = request.form.get('search_type')
        file_choice = request.form.get('file_choice')
        result_html = search_in_files(search_term, search_type, file_choice)
        return render_template('search.html', search_term=search_term, result_html=result_html, file_choice=file_choice)
    
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True, host='22.232.100.153', port=5015)
