from datetime import datetime
from sequences import get_next_value, get_last_value

class SeriesService():

    def __init__(self, **kwargs):
        self.application = kwargs.get('application')

    def generate_series(self):
            date = self.application.created_at
            formattedYear = date.strftime("%Y")[-2:]
            formattedDay = date.strftime("%m")
            series_id = ''
            if self.application.is_enrolled:
                series_id = get_next_value("rpt")
            else:
                series_id = get_next_value("bpl")
            series_id = f"{series_id}".zfill(5)
            series = 'OB%s%s-%s' % (formattedYear, formattedDay, series_id)
            return series

    def reset_series(self, sequence_name):
        last_value = get_last_value(sequence_name='rpt')
        reset_value = get_next_value(sequence_name='rpt',initial_value=0 ,reset_value=last_value)