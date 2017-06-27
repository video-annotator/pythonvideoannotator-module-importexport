import cv2
import pyforms #make sure the variable PYFORMS_USE_QT5 us loaded
from pysettings import conf

if conf.PYFORMS_USE_QT5:
	from PyQt5.QtWidgets import QFileDialog
else:
	from PyQt4.QtGui import QFileDialog

class ImportExportImage(object):


	def create_popupmenu_actions(self):
		
		self.tree.add_popup_menu_option(
			label='Import', 
			function_action=self.__import_image_window, 
			item=self.treenode, icon=conf.PYFORMS_ICON_EVENTTIMELINE_IMPORT
		)

		#self._value_import_window = GenericCsvParserDialog(['Frame', 'Value'])
		#self._value_import_window.load_file_event = self.__import_data_event

		self.tree.add_popup_menu_option("-", item=self.treenode)
		super(ImportExportImage,self).create_popupmenu_actions()

	def __import_image_window(self):
		value = QFileDialog.getOpenFileName(self, 'Select an image')
		value = value[0] if conf.PYFORMS_USE_QT5 else str(value)
		
		self.image = cv2.imread(value)