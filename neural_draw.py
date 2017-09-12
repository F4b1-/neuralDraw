#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from PIL import Image
from kivy.uix.label import Label
import scipy.ndimage
import neural_network
import os
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.checkbox import CheckBox
from kivy.properties import BooleanProperty


Builder.load_string('''
<ConfirmPopup>:
    cols:1
	Label:
		text: root.text
	GridLayout:
		cols: 2
		CheckBox:
			active: root.save_testdata_is_active
			on_press: root.toggle()
		Label:
			text: 'Save in training data'
	GridLayout:
		cols: 2
		size_hint_y: None
		Button:
			text: 'Yes'
			on_release: root.dispatch('on_answer','yes')
		Button:
			text: 'No'
			on_release: root.dispatch('on_answer', 'no')
''')

Builder.load_string('''
<CorrectionPopup>:
    cols:1
	Label:
		text: "Whoops, which number did you draw then?"
		size_hint_y: None
		height: '50sp'
	GridLayout:
		cols: 2
		Button:
			text: '0'
			on_release: root.dispatch('on_answer', '0')
		Button:
			text: '1'
			on_release: root.dispatch('on_answer', '1')
		Button:
			text: '2'
			on_release: root.dispatch('on_answer', '2')
		Button:
			text: '3'
			on_release: root.dispatch('on_answer', '3')
		Button:
			text: '4'
			on_release: root.dispatch('on_answer', '4')
		Button:
			text: '5'
			on_release: root.dispatch('on_answer', '5')
		Button:
			text: '6'
			on_release: root.dispatch('on_answer', '6')
		Button:
			text: '7'
			on_release: root.dispatch('on_answer', '7')
		Button:
			text: '8'
			on_release: root.dispatch('on_answer', '8')
		Button:
			text: '9'
			on_release: root.dispatch('on_answer', '9')
''')




class ConfirmPopup(GridLayout):
	text = StringProperty()

	save_testdata_is_active = BooleanProperty(True)
	
	def __init__(self,**kwargs):
		self.register_event_type('on_answer')
		super(ConfirmPopup,self).__init__(**kwargs)
		
	def on_answer(self, *args):
		pass

	def toggle(self):
        	self.save_testdata_is_active = not self.save_testdata_is_active

class CorrectionPopup(GridLayout):
	
	def __init__(self,**kwargs):
		self.register_event_type('on_answer')
		super(CorrectionPopup,self).__init__(**kwargs)
		
	def on_answer(self, *args):
		pass


class NeuralDrawWidget(Widget):

    def __init__(self, **kwargs):
        super(NeuralDrawWidget, self).__init__(**kwargs)
	self.rectPos = (188, 168)
	self.rectSize = (224, 224)
	self.lineWidth = 8
        with self.canvas:
            Color(1, 1, 1, 1)
            self.drawBackground()

    def drawBackground(self):
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.rectPos, size=self.rectSize)

    def on_touch_down(self, touch):
        with self.canvas:
            if self.isWithinRectangeBounds(touch):
                Color(0, 0, 0, 1)
                touch.ud['line'] = Line(points=(touch.x, touch.y),
                        width=self.lineWidth )

    def on_touch_move(self, touch):
        if self.isWithinRectangeBounds(touch):
            touch.ud['line'].points += [touch.x, touch.y]

    def isWithinRectangeBounds(self, touch):
	return touch.x < self.rectPos[0] + self.rectSize[0] - self.lineWidth  and touch.x > self.rectPos[0]  + self.lineWidth and  touch.y > self.rectPos[1] + self.lineWidth and touch.y < self.rectPos[1] + self.rectSize[1] - self.lineWidth

class NeuralDrawApp(App):


    def exportImg(self):
        self.painter.export_to_png('current.png')
	img = Image.open("current.png")
	size = 28, 28
	img2 = img.crop((188, 148, 412, 372))
	img2.thumbnail(size, Image.ANTIALIAS)
	img2.save("my_images/my_image.png")
	os.remove("current.png")

	self.neuralResult = str(neural_network.getResultFromInput())

	content= ConfirmPopup(text='You drew a: ' + self.neuralResult)
	content.bind(on_answer=self._on_answer)

	self.popup = Popup(title="Neural Net Result", content=content, auto_dismiss= False)

	self.popup.open()

    def _on_answer(self, instance, answer):

	if(answer == 'no' and self.popup.content.save_testdata_is_active):
		contentCorrection= CorrectionPopup()
		contentCorrection.bind(on_answer=self._on_answer_correction)
		self.popupCorrection = Popup(title="Neural Net Correction", content=contentCorrection, auto_dismiss= False)
		self.popupCorrection.open()
	elif self.popup.content.save_testdata_is_active:
		neural_network.saveImgToCSVFile(self.neuralResult)

	self.popup.dismiss()


    def _on_answer_correction(self, instance, answer):
	neural_network.saveImgToCSVFile(answer)		
	self.popupCorrection.dismiss()

    def build(self):
	parent = GridLayout(rows=2)
	parent2 = GridLayout(rows=3, size_hint_y=0.25)

        self.painter = NeuralDrawWidget()
        clearbtn = Button(text='Clear')
        analyzebtn = Button(text='Analyze')
        clearbtn.bind(on_release=self.clear_canvas)
        parent.add_widget(self.painter)

        parent2.add_widget(clearbtn)

        analyzebtn.bind(on_release=lambda x: self.exportImg())

        parent2.add_widget(analyzebtn)
        parent.add_widget(parent2)

        return parent

    def clear_canvas(self, obj):
        self.painter.drawBackground()


if __name__ == '__main__':
    Window.clearcolor = (0.7, 0.7, 0.7, 1)
    Window.size = (600, 540)
    NeuralDrawApp().run()


			
