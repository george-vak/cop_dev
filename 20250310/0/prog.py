class calend(cmd.Cmd):
    prompt = "calendar> "
    tc = calendar.TextCalendar()
    Month = {m.name: m.value for m in calendar.Month}

    def do_pryear(self, arg):
        """Print the calendar for an entrie year"""
        self.tc.pryaer(int(arg))
    
    def do_promonth(self, arg):
        year, month = arg.split()
        self.tc.promonth(int(year), self.Month[month])
    
    def complete_promonth(self, text, line, begidx, endidx):
        return [m for m in self.Month if m.startswith[(text)]]
    
    def do_EOF(self, arg):
        return True
