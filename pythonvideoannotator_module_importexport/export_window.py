import sys, os, shutil, re, pyforms, numpy as np, cv2
from pysettings 		 import conf
from pyforms 			 import BaseWidget
from pyforms.Controls 	 import ControlFile
from pyforms.Controls 	 import ControlPlayer
from pyforms.Controls 	 import ControlButton
from pyforms.Controls 	 import ControlNumber
from pyforms.Controls 	 import ControlSlider
from pyforms.Controls 	 import ControlList
from pyforms.Controls 	 import ControlCheckBox
from pyforms.Controls 	 import ControlText
from pyforms.Controls 	 import ControlCheckBoxList
from pyforms.Controls 	 import ControlEmptyWidget
from pyforms.Controls 	 import ControlProgress
from pyforms.Controls 	 import ControlTree


class ExportWindow(BaseWidget):

	def __init__(self, parent=None):
		BaseWidget.__init__(self, 'Export data', parent_win=parent)

		if conf.PYFORMS_USE_QT5:
			self.layout().setContentsMargins(5,5,5,5)
		else:
			self.layout().setMargin(5)
			
		self.setMinimumHeight(600)
		self.setMinimumWidth(800)

		self._tree		= ControlTree('Data')
		self._apply  	= ControlButton('Apply', checkable=True)
		self._progress 	= ControlProgress('Progress')
		self._add	    = ControlButton('Add')
		self._remove	= ControlButton('Remove')
		self._export_list = ControlList('Columns to export')
		self._file 		= ControlFile('Export to')

		
		self._formset = [
			[
				['_add','_tree'],'||', ['_remove','_export_list'],
			],
			'_file',
			'_apply',
			'_progress'
		]
		
		self._tree.show_header  = False

		self._add.value = self.__add_column_event
		self._remove.value = self.__remove_column_event
		
		self._apply.value 		= self.__apply_btn_event
		self._apply.icon 		= conf.ANNOTATOR_ICON_MOTION
		self._progress.hide()

		self._properties = []

	###########################################################################
	### EVENTS ################################################################
	###########################################################################

	def __field_full_name(self, tree_item):
		name = tree_item.text(0)
		while True:
			tree_item = tree_item.parent()
			if tree_item is None: break
			name = "{0} > {1}".format( tree_item.text(0) , name )
		return name

	def __add_column_event(self):
		item = self._tree.selected_item
		if hasattr(item, 'data_function'):
			self._export_list += [ self.__field_full_name(item) ]
			self._properties.append( (len(item.win), item.data_function) )

	def __remove_column_event(self):
		if self._export_list.selected_row_index>=0:
			self._properties.pop(self._export_list.selected_row_index)
			self._export_list -= -1
		
			
	def __apply_btn_event(self):

		if self._apply.checked:

			if self._file.value is None or len(self._file.value.strip())==0: 
				self._apply.checked = False
				return

			self._export_list.enabled 	= False
			self._tree.enabled 			= False
			self._add.enabled 			= False
			self._remove.enabled 		= False
			self._file.enabled 			= False
			self._apply.label 			= 'Cancel'

			total_2_analyse  = 0
			for n_frames, func in self._properties:
				if n_frames>total_2_analyse: total_2_analyse = n_frames

			self._progress.min = 0
			self._progress.max = total_2_analyse
			self._progress.show()



			filename = self._file.value

			with open(filename, 'w') as out:
				out.write('frame;')
				for values in self._export_list.value:
					out.write(('{0};'.format(values[0])) )
				out.write('\n')

				for index in range(total_2_analyse):
					out.write('{0};'.format(index))
					for _, func in self._properties:
						out.write( '{0};'.format(func(index)))
					out.write( '\n')
					self._progress.value = index
						
			
			self._export_list.enabled 	= True
			self._tree.enabled 			= True
			self._add.enabled 			= True
			self._remove.enabled 		= True
			self._file.enabled 			= True
			self._apply.label 		= 'Apply'
			self._apply.checked 	= False
			self._progress.hide()


	def __copy_tree_node(self, item, new_item):
		new_item.win = item.win
		if hasattr(item,'data_function'): new_item.data_function = item.data_function

	@property
	def project(self): return self._project
	@project.setter 
	def project(self, value): 
		self._project = value
		self._tree.clear()
		self._tree.clone_tree( value.tree, copy_function=self.__copy_tree_node )
		




	

if __name__ == "__main__": pyforms.start_app(ExportWindow)