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

    @staticmethod
    def from_action_text(action):
        return HTMLButton('', text=action.text, style=action.style, btn_type='submit')

    def __init__(self, name, icon='', text='', style='', size='', block=False, btn_type='', toggle='', target='', dismiss=''):
        super(HTMLButton, self).__init__('button', name)
        class_attr = ['btn']
        if style:
            class_attr.append("btn-"+style)
        if size:
            class_attr.append("btn-"+size)
        if block:
            class_attr.append("btn-block")
        self.root.set("class", " ".join(class_attr))
        if btn_type:
            self.root.set('type', btn_type)
        if toggle:
            self.root.set('data-toggle', toggle)
        if target:
            self.root.set('data-target', '#'+target)
        if dismiss:
            self.root.set('data-dismiss', dismiss)
        if icon:
            i = ET.Element('i')
            i.set('class', 'fa fa-'+icon)
            self.root.append(i)
        if text:
            self.root.text = text

class HTMLTable(HTMLObject):

    def __init__(self, name, columns, rows=[], actions=[], checkbox=True, filters=True, use_rest=None, use_cache=True):
        super(HTMLTable, self).__init__('table', name)
        self.root.set("class", "table table-bordred table-striped table-hover")
        header = ET.Element('thead')
        footer = ET.Element('tfoot')
        body = ET.Element('tbody')
        tr = ET.Element('tr')
        tr_foot = ET.Element('tr')
        tr.set("class", "headers")
        if checkbox:
            self.root.set("data-selectable", "true")
            th = ET.Element('th')
            chk = ET.Element('input')
            chk.set("type", "checkbox")
            chk.set("id", "checkall")
            th.append(chk)
            tr.append(th)
            tr_foot.append(ET.Element('th'))
        for column in columns:
            th = ET.Element('th')
            th.text = column[1]
            th.set("data-name", column[0])
            tr.append(th)
            tr_foot.append(th)
        if actions:
            for action in actions:
                th = ET.Element('th')
                th.set("class", "table-action")
                th.set("data-json", action.to_json())
                th.text = action.text
                tr.append(th)
                tr_foot.append(ET.Element('th'))
        header.append(tr)
        self.root.append(header)
        if filters:
            footer.append(tr_foot)
            self.root.append(footer)
        if use_rest:
            self.root.set("data-rest", use_rest)
            self.root.set("class", self.root.get('class')+" use-rest")
        if use_cache:
            self.root.set("use-cache", 'true')
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
                    td.text = str(row[column[0]])
                    tr.append(td)
                for field in row.keys():
                    tr.set("data-"+field, str(row[field]))
                if actions:
                    for action in actions:
                        td = ET.Element('td')
                        td.set("align", "center")
                        p = ET.Element('p')
                        p.set('data-pacement', "top")
                        p.set('data-toggle', 'tooltip')
                        p.set('title', action.text)
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

    def __init__(self, name, title, columns, rows=[], actions=[], checkbox=True, filters=True, buttons=[], use_rest=None, use_cache=True):
        super(Table, self).__init__("table")
        self.table = HTMLTable(name, columns, rows, actions, checkbox, filters, use_rest, use_cache)
        self.html = self.table.stringify()
        self.title = title
        self.buttons = buttons
        for button in self.buttons:
            button.root.set("class", button.root.get('class')+" btn-lg btn-block")

class Modal(Section):

    @staticmethod
    def from_action(action, body=[]):
        if action.name == 'multi-delete':
            body = [MultiDeleteInput, MultiDeleteAction, "Seguro que desea eliminar los elementos seleccionados?"]
        elif action.name == 'delete':
            body.append("Seguro que desea eliminar el elemento actual?")
        return Modal(action.name, action.text, buttons=[HTMLButton.from_action_text(action)], body=body, form_method=action.method)

    def __init__(self, name, title, buttons=[], add_close_btn=True, body=[], form_action='', form_method=''):
        super(Modal, self).__init__("modal")
        self.name = name
        self.title = title
        self.buttons = buttons
        self.form_action = form_action
        self.form_method = form_method
        self.body = []
        for item in body:
            self.body.append(ModalBodyItem(item))
        if add_close_btn:
            self.buttons.append(HTMLButton("", text="Close", style="default", dismiss='modal'))

    def add_form(self, form):
        self.body.append(ModalBodyItem(form))

class ModalBodyItem(Section):

    def __init__(self, item):
        super(ModalBodyItem, self).__init__("modal-body-item")
        self.type = item.__class__.__base__.__name__
        self.name = item.__class__.__name__
        self.obj = item


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

    MAP = {
        'edit':{
            "title": 'Editar',
            "icon": 'pencil',
            "level": 'success',
            "method": 'POST'
        },
        'delete':{
            "title":'Eliminar',
            "icon": 'trash',
            "level": 'danger',
            "method": 'POST'
        },
        'multi-delete':{
            "title":'Eliminar',
            "icon": 'trash',
            "level": 'danger',
            "method": 'POST'
        },
        'new':{
            "title":'Crear',
            "icon": 'plus-square',
            "level": 'primary',
            "method": 'POST'
        },
    }

    @staticmethod
    def crud_button(name):
        return Action(name, 'modal', text=Action.MAP[name]["title"], icon=Action.MAP[name]["icon"], style=Action.MAP[name]["level"], method=Action.MAP[name]["method"])

    @staticmethod
    def edit_and_delete():
        return [Action.crud_button('edit'), Action.crud_button('delete')]

    @staticmethod
    def new_and_multidelete():
        return [Action.crud_button('new'), Action.crud_button('multi-delete')]

    def __init__(self, name, action, text='', icon='', style='', method=''):
        self.name = name
        self.action = action
        self.text = text
        self.icon = icon
        self.style = style
        self.method = method

MultiDeleteInput = HTMLObject('input')
MultiDeleteInput.root.set('type', 'hidden')
MultiDeleteInput.root.set('name', 'ids')
MultiDeleteAction = HTMLObject('input')
MultiDeleteAction.root.set('type', 'hidden')
MultiDeleteAction.root.set('name', 'action')
MultiDeleteAction.root.set('value', 'multi-delete')
