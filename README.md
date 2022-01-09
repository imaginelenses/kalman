# kalman
A tool to implement and understand Kalman Filters.  

A Server-Client pair that reads the accelerometer readings from an Android device and sends them over to a desktop application over websockets. It then moves the cursor on the screen according to the change in acceleration of the mobile device.

Archived as there are problems with threading/multiprocessing while using `pythonautogui.moveRel()`

Check out [https://github.com/imaginelenses/kalmanDesk](https://github.com/imaginelenses/kalmanDesk)
