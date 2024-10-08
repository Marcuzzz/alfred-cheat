#!/usr/bin/python
from . import html_gen
from workflow.workflow import ICON_HELP as WARNINGICON
from workflow.workflow import ICON_NOTE as HINT


# Switches that autually controls the workflow behavior
class Options:

    LARGETEXTPATTERN = "{}\n\n{}"

    def __init__(self, parser, workflow):
        self._parser = parser
        self._workflow = workflow
        return None

    def search(self, sheetName, keyword):
        'Transmits the results of the keyword search in "sheetName" (everywhere sheetName==None) to Alfred workflow'
        if sheetName==None:
            ret=self._parser.searchAcrossAll(keyword, self._workflow)
            
            html_file = html_gen.create_html_global_search(ret,keyword,sheetName=None)
            tmp_filename = self._workflow.cachedir + "/search.html"
        else:
            if sheetName not in self._parser.availableSheets():
                Options.warning("Cheatsheet not found.","", self._workflow)
                return None
            ret=self._parser.searchInSheet(keyword, sheetName, self._workflow)
            
            html_file = html_gen.create_html_global_search(ret,keyword,sheetName)
            tmp_filename = self._workflow.cachedir + "/" + sheetName +'.html'
        if ret==[]:
            Options.warning("Not found", "No match found for search {}".format(keyword), self._workflow)
            return None
# Create HTML file
        file=open(tmp_filename,'wt')
        file.write(html_file)
        file.close
# Create Alfred entries
        for item in ret:
            type=item.get("type")
            if type=='entry':
                sheet=item.get("sheet",'')
                if sheet:
                    the_title="[" + sheet + "]  " + item.get("command")
                else:
                    the_title=item.get("command")
                    sheet=sheetName
                it=self._workflow.add_item(title=the_title,
                                        subtitle=item.get("comment"),
                                        largetext=item.get("comment")+"\n"+item.get("command"),
                                        copytext=item.get("command"),
                                        valid=True,
                                        arg=item.get("command"),
                                        quicklookurl=tmp_filename )
                it.add_modifier('cmd',  # or 'ctrl'?
                        subtitle='Open the "%s" cheat file in editor' % sheet,
                        valid=True,
                        arg= self._parser._sheetMapping.get(sheet),
                        )
        return None

    def list(self, sheetName):
        'Transmits all the entries of "sheetName" to Alfred workflow'
        ret=self._parser.list(sheetName)
        if ret==[]:
            Options.hint("Empty cheatsheet", "", self._workflow)
        
        tmp_filename = self._workflow.cachedir + "/" + sheetName +'.html'
        html_file = html_gen.create_html(ret)
        file=open(tmp_filename,'wt')
        file.write(html_file)
        file.close
        for item in ret:
            type=item.get("type")
            if type=="title":
                pass
            elif type=='section':
                pass
            elif type=='entry':
                it=self._workflow.add_item(title=item.get("command"),
                                        subtitle=item.get("comment"),
                                        largetext=item.get("comment")+"\n"+item.get("command"),
                                        valid=True,
                                        copytext=item.get("command"),
                                        arg=item.get("command"),
                                        quicklookurl=tmp_filename )
                it.add_modifier('cmd',  # or 'ctrl'?
                        subtitle='Open the "%s" cheat file in editor' % sheetName,
                        valid=True,
                        arg= self._parser._sheetMapping.get(sheetName),
                        )
        
        return None

    def showAvailable(self, sheetName=""):
        ret = self._FilterSheetName(sheetName)
        if ret == []:
            Options.warning("Cheat sheet not found.", "", self._workflow)
            return None
        for sheet in ret:
            self._workflow.add_item(
                    title=sheet,
                    autocomplete=sheet + " ",
                    largetext=sheet
                    ).add_modifier(
                    'cmd',
                    subtitle="open in editor",
                    valid=True,
                    arg=self._parser._sheetMapping.get(sheet))
        return None

    def _FilterSheetName(self, query):
        names = self._parser.availableSheets()
        return self._workflow.filter(query, names, key=lambda x: x)

    @staticmethod
    def warning(msg,subtitle,workflow):
        'Lets Alfred display a warning with (?) icon'
        workflow.warn_empty(
                title=msg,
                subtitle=subtitle,
                icon=WARNINGICON,
                )
        return None

    @staticmethod
    def hint(msg, subtitle, workflow):
        'Lets Alfred display a warning with (!) icon'
        workflow.warn_empty(
                title=msg,
                subtitle=subtitle,
                icon=HINT,
                )
        return None
