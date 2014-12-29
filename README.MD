OPERATING SYSTEMS<br>
ASSIGNMENT(s)<br>

Part I:  <br> 
	Design processor to take interactive processes and dispatch them to correct queues.<br>
	Grade: 9/10 (One trapping error / Resubmission)<br>
Part II:<br>
	Implement disc scheduling, FIFO for Processor and C-SCAN (Student choice) for the Disc queue.<br>
	Grade: 7/10 (Incorrect C-SCAN bugs on lab machines, seemed OK in tests but c'est la vie)<br>
Part III:<br>
	Implement memory management with Page Tables.<br>
	Grade 10/10<br>

Sysgen:<br>
	Follow instructions to generate the systems values.<br>
Running:<br>
	Commands:<br>
		A - Process Arrival<br>
		K# - Kill Process with PID#<br>
		p# - Send current Process (Head of ready queue) to Printer #<br>
		d# - Send current Process (Head of ready queue) to Disc #<br>
		r# - Send current Process (Head of ready queue) to #<br>
		P# - Send current Process (Head of printer queue #) to Ready Queue<br>
		D# - Send current Process (Head of disc queue #) to Ready Queue<br>
		R# - Send current Process (Head of  queue #) to Ready Queue<br>
		S - Generate Snapshot of Queues or memory<br>
			r,p,d,m<br>
<br>
WILLIAM WIDMER<br>
CSCI340<br>


PROGRAMMED IN PYTHON VERSION 2.7.6<br>
(Works with 2.7.5 which we use in eniac)<br>

Assuming process.py is the same directory.<br>
Run with any of these:<br>
	python main.py<br>
	sudo python main.py<br>
	python2.7 main.py<br>
	sudo python2.7 main.py<br>


Upon running your system may or may not create a process.pyc file.<br>

<br>
todo<br>
General<br>
- Cleaning up the code<br>

Programming<br>
- Fix the disc scheduler ala Professors critiques<br>
