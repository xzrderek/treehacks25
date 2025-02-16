import datetime
import platform
import subprocess

from tinyagent.src.tiny_agent.run_apple_script import run_applescript, run_applescript_capture


class Calendar:
    def __init__(self):
        self.calendar_app = "Calendar"

    def create_event(
        self,
        title: str,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        location: str = "",
        invitees: list[str] = [],
        notes: str = "",
        calendar: str | None = None,
    ) -> str:
        """
        Creates a new event with the given title, start date, end date, location, and notes.
        """
        if platform.system() != "Darwin":
            return "This method is only supported on MacOS"

        applescript_start_date = start_date.strftime("%B %d, %Y %I:%M:%S %p")
        applescript_end_date = end_date.strftime("%B %d, %Y %I:%M:%S %p")

        # Check if the given calendar parameter is valid
        if calendar is not None:
            script = f"""
            tell application "{self.calendar_app}"
                set calendarExists to name of calendars contains "{calendar}"
            end tell
            """
            exists = run_applescript(script)
            if not exists:
                calendar = self._get_first_calendar()
                if calendar is None:
                    return f"Can't find the calendar named {calendar}. Please try again and specify a valid calendar name."

        # If it is not provded, default to the first calendar
        elif calendar is None:
            calendar = self._get_first_calendar()
            if calendar is None:
                return "Can't find a default calendar. Please try again and specify a calendar name."

        invitees_script = []
        for invitee in invitees:
            invitees_script.append(
                f"""
                make new attendee at theEvent with properties {{email:"{invitee}"}}
            """
            )
        invitees_script = "".join(invitees_script)

        script = f"""
        tell application "System Events"
            set calendarIsRunning to (name of processes) contains "{self.calendar_app}"
            if calendarIsRunning then
                tell application "{self.calendar_app}" to activate
            else
                tell application "{self.calendar_app}" to launch
                delay 1
                tell application "{self.calendar_app}" to activate
            end if
        end tell
        tell application "{self.calendar_app}"
            tell calendar "{calendar}"
                set startDate to date "{applescript_start_date}"
                set endDate to date "{applescript_end_date}"
                set theEvent to make new event at end with properties {{summary:"{title}", start date:startDate, end date:endDate, location:"{location}", description:"{notes}"}}
                {invitees_script}
                switch view to day view
                show theEvent
            end tell
            tell application "{self.calendar_app}" to reload calendars
        end tell
        """

        try:
            run_applescript(script)
            return f"""Event created successfully in the "{calendar}" calendar."""
        except subprocess.CalledProcessError as e:
            return str(e)

    def _get_first_calendar(self) -> str | None:
        script = f"""
            tell application "System Events"
                set calendarIsRunning to (name of processes) contains "{self.calendar_app}"
                if calendarIsRunning is false then
                    tell application "{self.calendar_app}" to launch
                    delay 1
                end if
            end tell
            tell application "{self.calendar_app}"
                set firstCalendarName to name of first calendar
            end tell
            return firstCalendarName
            """
        stdout = run_applescript_capture(script)
        if stdout:
            return stdout[0].strip()
        else:
            return None

    def get_next_meeting(self) -> dict:
        """
        Gets the next meeting's end time from the calendar.
        Returns a dictionary with the end time in format 'YYYY-MM-DD HH:MM:SS'
        """
        if platform.system() != "Darwin":
            return {"error": "This method is only supported on MacOS"}

        script = f"""
        set currentDate to current date
        tell application "{self.calendar_app}"
            set targetCalendar to first calendar
            set nextEvent to missing value

            repeat with e in (every event of targetCalendar whose start date is greater than currentDate)
                if nextEvent is missing value then
                    set nextEvent to e
                else if (start date of e) is less than (start date of nextEvent) then
                    set nextEvent to e
                end if
            end repeat

            if nextEvent is not missing value then
                set endDate to end date of nextEvent
                -- Format the date as required
                set y to year of endDate as string
                set m to text -2 thru -1 of ("0" & (month of endDate as integer as string))
                set d to text -2 thru -1 of ("0" & (day of endDate as string))
                set h to text -2 thru -1 of ("0" & (hours of endDate as string))
                set min to text -2 thru -1 of ("0" & (minutes of endDate as string))
                set s to text -2 thru -1 of ("0" & (seconds of endDate as string))
                
                return y & "-" & m & "-" & d & " " & h & ":" & min & ":" & s as string
            else
                return "error|No upcoming meetings"
            end if
        end tell
        """

        try:
            result = run_applescript_capture(script)
            if result and not result[0].startswith("error|"):
                return {"end_date": result[0].strip()}
            return {"error": result[0].split("|")[1].strip() if result and "|" in result[0] else "No upcoming meetings found"}
        except Exception as e:
            print("DEBUG, ERROR: ", e)
            return {"error": f"Error reading calendar: {str(e)}"}
