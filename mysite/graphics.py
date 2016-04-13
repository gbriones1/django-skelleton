import json

from xml.etree import ElementTree as ET

class HTMLObject(object):

    def __init__(self, tag='div', name=''):
        self.tag = tag
        self.root = ET.Element(self.tag)
        if name:
            self.root.set("id", name)

    def stringify(self):
        return ET.tostring(self.root, method='html')


class HTMLButton(HTMLObject):

    @staticmethod
    def from_action(action):
        return HTMLButton('', icon=action.icon, style=action.style, toggle=action.action, target=action.name)

    def __init__(self, name, icon='', text='', style='', size='', block=False, toggle='', target=''):
        super(HTMLButton, self).__init__('button', name)
        class_attr = ['btn']
        if style:
            class_attr.append("btn-"+style)
        if size:
            class_attr.append("btn-"+size)
        if block:
            class_attr.append("btn-block")
        self.root.set("class", " ".join(class_attr))
        if toggle:
            self.root.set('data-toggle', toggle)
        if target:
            self.root.set('data-target', '#'+target)
        if icon:
            i = ET.Element('i')
            i.set('class', 'fa fa-'+icon)
            self.root.append(i)
        if text:
            self.root.text = text

class HTMLTable(HTMLObject):

    def __init__(self, name, columns, rows=[], actions=[], checkbox=True, use_rest=None):
        super(HTMLTable, self).__init__('table', name)
        self.root.set("class", "table table-bordred table-striped table-hover")
        header = ET.Element('thead')
        body = ET.Element('tbody')
        tr = ET.Element('tr')
        tr.set("class", "headers")
        if checkbox:
            self.root.set("data-selectable", "true")
            th = ET.Element('th')
            chk = ET.Element('input')
            chk.set("type", "checkbox")
            chk.set("id", "checkall")
            th.append(chk)
            tr.append(th)
        for column in columns:
            th = ET.Element('th')
            th.text = column[1]
            th.set("data-name", column[0])
            tr.append(th)
        if actions:
            for action in actions:
                th = ET.Element('th')
                th.set("class", "table-action")
                th.set("data-json", action.to_json_attr())
                th.text = Action.TITLES[action.name]
                tr.append(th)
        header.append(tr)
        self.root.append(header)
        if use_rest:
            self.root.set("data-rest", use_rest)
            self.root.set("class", self.root.get('class')+" use-rest")
        else:
            for row in rows:
                tr = ET.Element('tr')
                if checkbox:
                    td = ET.Element('td')
                    chk = ET.Element('input')
                    chk.set("type", "checkbox")
                    chk.set("class", "checkthis")
                    td.append(chk)
                    tr.append(td)
                for column in columns:
                    td = ET.Element('td')
                    td.text = row[column[0]]
                    tr.append(td)
                if actions:
                    for action in actions:
                        td = ET.Element('td')
                        td.set("align", "center")
                        p = ET.Element('p')
                        p.set('data-pacement', "top")
                        p.set('data-toggle', 'tooltip')
                        p.set('title', Action.TITLES[action.name])
                        button = HTMLButton.from_action(action)
                        p.append(button.root)
                        td.append(p)
                        tr.append(td)
                body.append(tr)
        self.root.append(body)

class Section(object):

    def __init__(self, section):
        self.section = section


class Table(Section):

    def __init__(self, name, title, columns, rows=[], actions=[], checkbox=True, buttons=[], use_rest=None):
        super(Table, self).__init__("table")
        self.table = HTMLTable(name, columns, rows, actions, checkbox, use_rest)
        self.html = self.table.stringify()
        self.title = title


class HelperObject(object):

    def to_json(self):
        string = ''
        try:
            string = json.dumps(self, default=lambda x: x.__dict__)
        except:
            pass
        return string

    def to_json_attr(self):
        result = {}
        json_str = self.to_json()
        if json_str:
            attrs = json.loads(json_str)
            for key in attrs.keys():
                result["data-"+key] = attrs[key]
        return json.dumps(result)

class Action(HelperObject):

    CRUD_ACTIONS = {
        'edit':('pencil', 'success'),
        'delete':('trash', 'danger'),
        'multi-delete':('trash', 'danger'),
        'new':('plus-square', 'primary'),
    }
    TITLES = {
        'edit':'Editar',
        'delete':'Eliminar',
        'multi-delete':'Eliminar',
        'new':'Crear',
    }

    @staticmethod
    def crud_button(name):
        return Action(name, 'modal', icon=Action.CRUD_ACTIONS[name][0], style=Action.CRUD_ACTIONS[name][1])

    @staticmethod
    def edit_and_delete():
        return [Action.crud_button('edit'), Action.crud_button('delete')]

    @staticmethod
    def new_and_multidelete():
        return [Action.crud_button('new'), Action.crud_button('multi-delete')]

    def __init__(self, name, action, text='', icon='', style=''):
        self.name = name
        self.action = action
        self.text = text
        self.icon = icon
        self.style = style
