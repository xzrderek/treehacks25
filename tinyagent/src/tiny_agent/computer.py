from tinyagent.src.tiny_agent.tools.calendar import Calendar
from tinyagent.src.tiny_agent.tools.contacts import Contacts
from tinyagent.src.tiny_agent.tools.mail import Mail
from tinyagent.src.tiny_agent.tools.maps import Maps
from tinyagent.src.tiny_agent.tools.notes import Notes
from tinyagent.src.tiny_agent.tools.reminders import Reminders
from tinyagent.src.tiny_agent.tools.sms import SMS
from tinyagent.src.tiny_agent.tools.spotlight_search import SpotlightSearch
from tinyagent.src.tiny_agent.tools.zoom import Zoom


class Computer:
    calendar: Calendar
    contacts: Contacts
    mail: Mail
    maps: Maps
    notes: Notes
    reminders: Reminders
    sms: SMS
    spotlight_search: SpotlightSearch
    zoom: Zoom

    def __init__(self) -> None:
        self.calendar = Calendar()
        self.contacts = Contacts()
        self.mail = Mail()
        self.maps = Maps()
        self.notes = Notes()
        self.reminders = Reminders()
        self.sms = SMS()
        self.spotlight_search = SpotlightSearch()
