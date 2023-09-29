import dash
import plotly.express as px
from dash import dcc, html, Input, Output
from dash import dash_table
import pandas as pd
import os

app = dash.Dash(__name__)

# Get the absolute path to the CSV file
csv_file_path = os.path.join(os.path.dirname(__file__), 'student.csv')

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Replace 'fifth' with 'five' in the 'class' column and simultaneously update the df
df['class'] = df['class'].replace('Fifth', 'Five')

df1 = pd.DataFrame({
    'Class': df['class'],
    'Score': df['mark']
})

class_mean_marks = df.groupby('class')[
    'mark'].mean().reset_index()  # find the mean marks per class, original without any arbitrary number

# this dataframe has the class and respective mean marks
df2 = pd.DataFrame({
    'Class': class_mean_marks['class'],
    'Average Score': class_mean_marks['mark']
})

# unique values for the dropdown
class_options = [{'label': cls, 'value': cls} for cls in df['class'].unique()]

# unique id to check at random
id_options = [{'label': identity, 'value': identity} for identity in df['id'].unique()]

# Define the layout
app.layout = html.Div(children=[
    html.H1(children="Examination Results"),

    html.Div(children='''
        Enter an arbitrary mark in your FIRST class of choice to see the new average!
    '''),

    html.Div([
        dcc.Dropdown(
            id='class-dropdown-1',
            options=class_options,
            value='Five',  # Default to 'Five'
        ),
        dcc.Input(
            id='user-input-1',
            type='number',
            placeholder='Enter marks...',
            value=0,  # Changed the default value to a number
        ),

        html.Div(children='''
         Enter an arbitrary mark in your SECOND class of choice to see the new average!
         '''),

        dcc.Dropdown(
            id='class-dropdown-2',
            options=class_options,
            value='Five',  # Default to 'Five'
        ),
        dcc.Input(
            id='user-input-2',
            type='number',
            placeholder='Enter marks...',
            value=0,  # Changed the default value to a number
        ),

        html.Div(children='''
         Enter an arbitrary mark in your THIRD class of choice to see the new average!
         '''),

        dcc.Dropdown(
            id='class-dropdown-3',
            options=class_options,
            value='Five',  # Default to 'Five'
        ),
        dcc.Input(
            id='user-input-3',
            type='number',
            placeholder='Enter marks...',
            value=0,  # Changed the default value to a number
        ),

        html.Div(id='average-score-output')  # Display the updated average score here
    ]),

    # the table elements with unique IDs
    html.Div([
        html.H2("Classes and Score Sheet", style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='table1',
            columns=[{'name': col, 'id': col} for col in df1.columns],
            data=df1.to_dict('records'),
            style_table={'height': '300px', 'overflowY': 'auto'}
        ),
    ], style={'display': 'inline-block', 'width': '40%', 'padding': '20px'}),

    html.Div([
        html.H2("Classes and Average Scores", style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='table2',
            columns=[{'name': col, 'id': col} for col in df2.columns],
            data=df2.to_dict('records'),
            style_table={'height': '300px', 'overflowY': 'auto'}
        ),
    ], style={'display': 'inline-block', 'width': '40%', 'padding': '20px'}),

    html.Div([
        html.H2("Bar Chart of Mean Score by Class Name", style={'textAlign': 'center'}),
        dcc.Graph(
            id='bar-chart',
            figure=px.bar(
                df2,
                x='Class',
                y='Average Score',
                labels={'Class': 'Class', 'Average Score': 'Mean Marks'},
                title='Mean Marks by Class'
            )
        ),
    ], style={'width': '80%', 'padding': '20px', 'margin': '0 auto'}),

    html.Div([
        html.H2("Pie Chart of Class Distribution", style={'textAlign': 'center'}),
        dcc.Graph(
            id='pie-chart',
            figure=px.pie(
                df,
                names='id',
                values='mark',
                labels={'id': 'ID'},
                title=f'Marks Distribution for Student ID in Class'
            )
        ),
    ], style={'width': '80%', 'display': 'inline-block', 'padding': '20px', 'margin': '0 auto'}),

    html.Div([
        html.H2("Select student ID", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='class-dropdown-4',
            options=class_options,
            value='Five',  # Default to 1, an integer NOT A STRING
        ),
    ], style={'width': '30%', 'padding': '20px', 'margin': '0 auto'}),
])


# Callback to update df1, df2, and the bar chart when the user selects a class and enters marks
@app.callback(
    Output('table1', 'data'),
    Output('table2', 'data'),
    Output('average-score-output', 'children'),
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('class-dropdown-1', 'value'),
    Input('user-input-1', 'value'),
    Input('class-dropdown-2', 'value'),
    Input('user-input-2', 'value'),
    Input('class-dropdown-3', 'value'),
    Input('user-input-3', 'value'),
    Input('class-dropdown-4', 'value'),
)
def update_data(selected_class1, entered_mark1, selected_class2, entered_mark2, selected_class3, entered_mark3,
                selected_class4):
    if selected_class4 is not None:
        # update the dataframe df to only show the rows for the selected id and the class
        class_data = df[df['class'] == selected_class4]

        pie_chart = px.pie(
            class_data,
            names='id',
            values='mark',
            labels={'id': 'ID'},
            title=f'Marks Distribution for Student ID in Class {selected_class4}'
        )
    else:
        pie_chart = px.pie(df, names='id', values='mark', labels={'id': 'ID'},
                           title='Marks Distribution according to ID')

    if selected_class1 is not None and entered_mark1 is not None:
        # Append user's first input data to df1
        new_data1 = {'Class': [selected_class1], 'Score': [float(entered_mark1)]}
        df1_updated = pd.concat([df1, pd.DataFrame(new_data1)], ignore_index=True)

        if selected_class2 is not None and entered_mark2 is not None:
            # Append user's second input data to df1, update the same dataframe
            new_data2 = {'Class': [selected_class2], 'Score': [float(entered_mark2)]}
            df1_updated = pd.concat([df1_updated, pd.DataFrame(new_data2)], ignore_index=True)

            if selected_class3 is not None and entered_mark3 is not None:
                # Append user's third input data to df1, update the same dataframe
                new_data3 = {'Class': [selected_class3], 'Score': [float(entered_mark3)]}
                df1_updated = pd.concat([df1_updated, pd.DataFrame(new_data3)], ignore_index=True)

        # Update df2 with the new mean marks
        class_average_marks = df1_updated.groupby('Class')['Score'].mean().reset_index()
        df2_updated = pd.DataFrame({
            'Class': class_average_marks['Class'],
            'Average Score': class_average_marks['Score']
        })

        # Update the first and second tables with the class and the scores
        table_data_1 = df1_updated.to_dict('records')
        table_data_2 = df2_updated.to_dict('records')
        confirmation_message = f'Virtual marks for Class {selected_class1}: {entered_mark1},\nClass {selected_class2}:{entered_mark2},\nClass {selected_class3}:{entered_mark3}'

        # Update the bar chart with df2_updated data
        updated_bar_chart = px.bar(
            df2_updated,
            x='Class',
            y='Average Score',
            labels={'Class': 'Class', 'Average Score': 'Mean Marks'},
            title='Mean Marks by Class'
        )
    else:
        table_data_1 = df1.to_dict('records')
        table_data_2 = df2.to_dict('records')
        confirmation_message = ''
        updated_bar_chart = px.bar(
            df2,
            x='Class',
            y='Average Score',
            labels={'Class': 'Class', 'Average Score': 'Mean Marks'},
            title='Mean Marks by Class'
        )

    return table_data_1, table_data_2, confirmation_message, updated_bar_chart, pie_chart


if __name__ == '__main__':
    app.run_server(debug=True)
