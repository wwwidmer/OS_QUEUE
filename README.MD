OPERATING SYSTEMS
ASSIGNMENT(s)

Part I: 
	Design processor to take interactive processes and dispatch them to correct queues.
	Grade: 9/10 (One trapping error / Resubmission)
Part II:
	Implement disc scheduling, FIFO for Processor and C-SCAN (Student choice) for the Disc queue.
	Grade: 7/10 (Incorrect C-SCAN bugs on lab machines, seemed OK in tests but c'est la vie)
Part III:
	Implement memory management with Page Tables.
	Grade 10/10

Sysgen:
	Follow instructions to generate the systems values.
Running:
	Commands:
		A - Process Arrival
		K# - Kill Process with PID#
		p# - Send current Process (Head of ready queue) to Printer #
		d# - Send current Process (Head of ready queue) to Disc #
		r# - Send current Process (Head of ready queue) to #
		P# - Send current Process (Head of printer queue #) to Ready Queue
		D# - Send current Process (Head of disc queue #) to Ready Queue
		R# - Send current Process (Head of  queue #) to Ready Queue
		S - Generate Snapshot of Queues or memory
			r,p,d,m

WILLIAM WIDMER
CSCI340


PROGRAMMED IN PYTHON VERSION 2.7.6
(Works with 2.7.5 which we use in eniac)

Assuming process.py is the same directory.
Run with any of these:
	python main.py
	sudo python main.py
	python2.7 main.py
	sudo python2.7 main.py


Upon running your system may or may not create a process.pyc file.


todo
General
- Cleaning up the code

Programming
- Fix the disc scheduler ala Professors critiques
