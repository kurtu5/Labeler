Problems:
	Turning a big flat jupyter notebook of my initial MVP attempt(that worked) into seperate folders/files for
		organization.   imports to glue this code together are killing me.

	My MVP implementation is weak and needs better separation and I can work on that when I figure out how to
		handle imports

	Features beyond just showing images in the Gui are not implemented yet.

	Unit tests are being held up by my poor understanding of python3.6 importing

Basic structure.
Labler is the package to be run as python -m Labeler
	App exists to separate code
		MVPBase contains base classes for the MVP framework
		All other subdirs are MVP derived classes to implement MVP for the App
			Example; Gui draws main win, has Menubar, has StatusBar
			         Labeler is the window where you label
			         Options is the options window
                                 ... and etc ...
		

.
├── bin
├── Labeler
│   ├── App
│   │   ├── _App.py
│   │   ├── GenericWindow
│   │   │   ├── __init__.py
│   │   │   ├── Model.py
│   │   │   ├── Presenter.py
│   │   │   └── View.py
│   │   ├── GradingWindow
│   │   │   ├── __init__.py
│   │   │   ├── Model.py
│   │   │   ├── Presenter.py
│   │   │   └── View.py
│   │   ├── Gui
│   │   │   ├── __init__.py
│   │   │   ├── Model.py
│   │   │   ├── Presenter.py
│   │   │   ├── __pycache__
│   │   │   │   ├── GuiModel.cpython-36.pyc
│   │   │   │   ├── GuiPresenter.cpython-36.pyc
│   │   │   │   ├── GuiView.cpython-36.pyc
│   │   │   │   ├── __init__.cpython-36.pyc
│   │   │   │   ├── Model.cpython-36.pyc
│   │   │   │   ├── Presenter.cpython-36.pyc
│   │   │   │   └── View.cpython-36.pyc
│   │   │   ├── test.py
│   │   │   └── View.py
│   │   ├── Images
│   │   │   ├── __init__.py
│   │   │   ├── Model.py
│   │   │   ├── Presenter.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-36.pyc
│   │   │   │   ├── Model.cpython-36.pyc
│   │   │   │   ├── Presenter.cpython-36.pyc
│   │   │   │   └── View.cpython-36.pyc
│   │   │   └── View.py
│   │   ├── __init__.py
│   │   ├── LabelerWindow
│   │   │   ├── __init__.py
│   │   │   ├── Model.py
│   │   │   ├── Presenter.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-36.pyc
│   │   │   │   ├── Presenter.cpython-36.pyc
│   │   │   │   └── View.cpython-36.pyc
│   │   │   └── View.py
│   │   ├── MenuBar
│   │   │   ├── __init__.py
│   │   │   ├── Model.py
│   │   │   ├── Presenter.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-36.pyc
│   │   │   │   ├── Model.cpython-36.pyc
│   │   │   │   ├── Presenter.cpython-36.pyc
│   │   │   │   └── View.cpython-36.pyc
│   │   │   └── View.py
│   │   ├── MVPBase
│   │   │   ├── Command.py
│   │   │   ├── __init__.py
│   │   │   ├── Interactor.py
│   │   │   ├── Model.py
│   │   │   ├── Observable.py
│   │   │   ├── Presenter.py
│   │   │   ├── __pycache__
│   │   │   │   ├── Command.cpython-36.pyc
│   │   │   │   ├── __init__.cpython-36.pyc
│   │   │   │   ├── Interactor.cpython-36.pyc
│   │   │   │   ├── Model.cpython-36.pyc
│   │   │   │   ├── Observable.cpython-36.pyc
│   │   │   │   ├── Presenter.cpython-36.pyc
│   │   │   │   └── View.cpython-36.pyc
│   │   │   └── View.py
│   │   ├── OptionsWidow
│   │   │   ├── __init__.py
│   │   │   ├── Model.py
│   │   │   ├── Presenter.py
│   │   │   └── View.py
│   │   ├── __pycache__
│   │   │   ├── _App.cpython-36.pyc
│   │   │   ├── App.cpython-36.pyc
│   │   │   └── __init__.cpython-36.pyc
│   │   ├── test.py
│   │   ├── TestWindow
│   │   │   ├── __init__.py
│   │   │   ├── Model.py
│   │   │   ├── Presenter.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-36.pyc
│   │   │   │   ├── Model.cpython-36.pyc
│   │   │   │   ├── Presenter.cpython-36.pyc
│   │   │   │   └── View.cpython-36.pyc
│   │   │   └── View.py
│   │   └── tkCustom
│   │       ├── AutoScrollBar.py
│   │       ├── AutoSizeGrip.py
│   │       ├── Bind.py
│   │       └── StatusBar.py
│   ├── Docs
│   │   └── readme.txt
│   ├── imports.py
│   ├── __init__.py
│   ├── _Labeler.py
│   ├── __main__.py
│   ├── __pycache__
│   │   ├── core.cpython-36.pyc
│   │   ├── __init__.cpython-35.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── __main__.cpython-35.pyc
│   │   └── mod.cpython-36.pyc
│   └── test.py
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
└── test.py

22 directories, 96 files
# OOP Strategy
## Overview
### Desc
https://wiki.wxpython.org/ModelViewPresenter   good overview in wx  and shows V<->P event Interactor class
http://wiki.c2.com/?ModelViewPresenter   simple descrip
http://duganchen.ca/mvp-with-pyqt-with-a-model-layer/   I dont like this really because events are connected in the main initilization instead of being encapsulated in a generic interactor class.... but perhaps i take the gtsignal concept and put it into a Interactor


MVP
  View takes input and knows its (UPDATE only itself)presenter
      it has getters and setters for the presenter...
      ONLY store GUI stuff, dont do data reprocessing(let presenter do that)
      inteligently deal with events and send event to Presenter
      MORE:  Interactor class sets binds and tells Presenter to do generic updates
                  these updates just do a whole(redraw view based on model, whatever widgets in view are set to, apply thier vals to model)
      
  Presenter knows its view, processes input from View and redraws view based on model
      Format data appropriately for View or for model
      process evens and update Model
      watch model for changes and send any appropriate updates to View
      More:  apparently there is a Command layer to make model changes
              and a Selection layer to know what elements of the model Command interacts with

  Model knows its presenter and will task it to update if it changes
      wait for events from Presenter
      can be modified by other models(specific changes will be sent to it's presenter as below)
      send events to presenter for specific changes
      
      init
      M() starts uninitialized
      V() starts uninitialized
      P(M,V) registers with M,V for bidirectional comm
          obeservable class allows presenter to see changes in M and in v?
          
  Multiwindows   load all views presenters and models
  
     create initial GUIView  GUI has menubar, currentwindow and statusbar
     GUIPresenter takes to GUIpresenter to manage window state
     GUIModel has list of models,  window_current and initial_window
     
     LabelerV  page to label images
     LabelerP handles inputs if models says its active.  renders images
     LabelerM handles loading images, setting current, cycling images(from events)
     
     OptionsView  page to set options(path, csv dir, shorcuts)
     OptionsP
     OptionsM
     
     PandasV   display data
     PandasP
     PandasM   stores the data
     
     #Future
     ClassifyV   run classifier on unlabled using labeled data so far
     
     GradePredictionsV grade the results of classification
     
     ClassifierOptionsV  change how clssifier works, save/load trainedmodels etc


## Basic start

     app.main
         instantiate all models into models{}
             each model is given its PresenterClass and list of other models
         instantiate all presenter into presenter{}
             each presenter is given its modelclass and viewclass
         instantiate all views into views{}
             each view is given its presenter
             
         # Start things?   i.e. at instantiation a model have know the class of its presenter but it may have had to tell that presenter to do soething at start, but that class may not have been instantiated at the model's time of instantiation 
         
         mainloop()
         
##  Example things going on;

      guimodel defaults to labelerview as the current window and also has set lablerM as is_active 
      current_window is monitored guiP
        it then tells guiview to raise the window
      GuiP registers escape to close window
      
      the labelerview raises and it's presenter has allready been told by labelermodel that its current image is something so it has displayed an initial image
      
     also since labelerM is_acbtive so to tells labelerP to tell labelerV to bind for events and send them to itself
     next,previos now work... LabelerP get these and tells LabelerM to cycle images, when LabelerM has done so LabelerP picks up on that and updates LabelerV
     
     lables on the image have also been drawn.   labelerM was initially set to some shortcuts.   this set told labelerP to draw them in LabelerV
     
     shorcut key events are sent to LabelerP, then to LabelerM to store them, and the change then caused LabelerP to tell LabelerV to redraw
     
                              

































