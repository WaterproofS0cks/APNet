import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from RetrieveDatabase import dbRetrieve

class dbChart:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.db_retrieve = dbRetrieve(self.db_connection)
        
    def date_range(self, duration):
        current_date = datetime.now()
        chosen_date = current_date - relativedelta(**{duration[0]: duration[1]})
        return chosen_date



    def retrieve_data(self, duration, tablename, column):
        base_date = self.date_range(duration)
        data = self.db_retrieve.retrieve(
            tablename, 
            f"{column}::DATE, COUNT(*)", 
            f"{column} BETWEEN %s AND CURRENT_DATE" + f" GROUP BY {column}::DATE ORDER BY {column}::DATE", 
            (base_date,)
        ) 
        return data
    
    def plot_registration_graph(self, duration, tablename, column, xLabel, yLabel, title, lineLabel):
        if duration[0] == "all-time":
            user_data = self.db_retrieve.retrieve_data_all(tablename, column)
        else:
            user_data = self.retrieve_data(duration, tablename, column)

        if not user_data:
            dates = []
            user_count = []
        else:
            dates = [record[0] for record in user_data]
            user_count = [record[1] for record in user_data]

        if duration[0] == "all-time" and dates:
            base_date = min(dates)
        else:
            base_date = self.date_range(duration).date()

        if dates:
            last_date = max(dates)
            all_dates = [base_date + timedelta(days=i) for i in range((last_date - base_date).days + 1)]
        else:
            all_dates = [base_date - timedelta(days=1)]

        all_user_count = [0] * len(all_dates)

        for i, date in enumerate(all_dates):
            if date in dates:
                index = dates.index(date)
                all_user_count[i] = user_count[index]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=all_dates,
            y=all_user_count,
            mode='lines',
            name=lineLabel
        ))

        num_dates = len(all_dates)
        if num_dates <= 2:
            tickvals = all_dates
        else:
            tickvals = [all_dates[i] for i in range(0, num_dates, max(1, num_dates // 5))]
  
        fig.update_layout(
            title=f"{title} - Last {duration[1]} {duration[0]}",
            xaxis_title=xLabel,
            yaxis_title=yLabel,
            xaxis=dict(
                type='date',
                tickformat='%Y-%m-%d',
                tickangle=45,
                automargin=True,
                tickvals=tickvals,
                ticktext=[date.strftime('%Y-%m-%d') for date in tickvals] 
            ),
            yaxis=dict(
                tickmode='linear',
                dtick=1,
                range=[0, max(all_user_count) + 1 if all_user_count else 1]
            ),
            showlegend=True
        )

        return fig.to_html(full_html=False)