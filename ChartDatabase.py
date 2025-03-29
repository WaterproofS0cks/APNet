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
            (base_date.date(),)
        ) 
        return data
    
    def plot_graph(self, duration, tablename, column, xLabel, yLabel, title, lineLabel):
        if duration[0] == "all-time":
            user_data = self.db_retrieve.retrieve_data_all(tablename, column)
        else:
            user_data = self.retrieve_data(duration, tablename, column)

        today = datetime.today().date()
        yesterday = today - timedelta(days=1)

        if not user_data:
            dates = [yesterday, today]
            user_count = [0, 0]
        else:
            dates = [record[0] for record in user_data]
            user_count = [record[1] for record in user_data]

        if duration[0] == "all-time" or duration[0] == "days":
            if len(dates) == 1:
                if dates[0] != today:
                    dates.append(today)
                    user_count.append(0)
                if dates[0] != yesterday:
                    dates.insert(0, yesterday)
                    user_count.insert(0, 0)
            base_date = min(dates)
        else:
            base_date = self.date_range(duration).date()

        if dates:
            last_date = max(dates)
            all_dates = [base_date + timedelta(days=i) for i in range((last_date - base_date).days + 1)]
        else:
            all_dates = [yesterday, today]

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

        max_y = max(all_user_count, default=0)
        y_step = max(1, max_y // 6)

        if (max_y // y_step) > 5:
            y_step = max(1, max_y // 5)

        max_y = (max_y // y_step + 1) * y_step
        y_axis_range = [0, max_y + 1]

        num_dates = len(all_dates)
        if num_dates <= 2:
            tickvals = all_dates
        else:
            tickvals = [all_dates[i] for i in range(0, num_dates, max(1, num_dates // 5))]

        fig.update_layout(
            title=f"{title} - Past {duration[0]}",
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
                dtick=y_step,
                range=y_axis_range  
            ),
            showlegend=True
        )

        return fig.to_html(full_html=False)

    def set_graph(self, database, filter):
        if database == "users":
            duration = (filter, 1)
            tablename = database
            column="registerdate" 
            xLabel="Date"
            yLabel="Number Of Users"
            title="Registered Users Over Time"
            lineLabel="Registered Users"

        elif database == "post":
            duration = (filter, 1)
            tablename = database
            column="timestamp" 
            xLabel="Date"
            yLabel="Number Of Posts"
            title="Post Created Over Time"
            lineLabel="Created Post"

        elif database == "postcomment":
            duration = (filter, 1)
            tablename = database
            column="timestamp"
            xLabel="Date"
            yLabel="Number Of Comments"
            title="Comments Over Time"
            lineLabel="Comments"

        elif database == "recruitment":
            duration = (filter, 1)
            tablename = database
            column="timestamp"
            xLabel="Date"
            yLabel="Number Of Recruitment Created"
            title="Recruitment Created Over Time"
            lineLabel="Recruitment Created"

        elif database == "application":
            duration = (filter, 1)
            tablename = database
            column="timestamp"
            xLabel="Date"
            yLabel="Number Of Applications"
            title="Application Over Time"
            lineLabel="Application Applied"

        elif database == "penaltyhistory":
            duration = (filter, 1)
            tablename = database
            column="timestamp"
            xLabel="Date"
            yLabel="Number Of Moderation"
            title="Moderation Over Time"
            lineLabel="Users Moderation"

        elif database == "reports":
            duration = (filter, 1)
            tablename = database
            column="timestamp"
            xLabel="Date"
            yLabel="Number Of Reports"
            title="Reports Over Time"
            lineLabel="Reports"

        elif database == "activity":
            duration = (filter, 1)
            tablename = database
            column="timestamp"
            xLabel="Date"
            yLabel="User Activity"
            title="Activity Over Time"
            lineLabel="Activity"

        else:
            duration = ("all-time", 1)
            tablename = "users"
            column="registerdate"
            xLabel="Registration Date"
            yLabel="Number Of Users"
            title="Registered Users Over Time"
            lineLabel="Registered Users"

        return self.plot_graph(duration, tablename, column, xLabel, yLabel, title, lineLabel)

