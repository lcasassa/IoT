run:
	python device.py

input0_true:
	echo 1 > input0.txt

input0_false:
	echo 0 > input0.txt

input1_true:
	echo 1 > input1.txt

input1_false:
	echo 0 > input1.txt

clean:
	rm input0.txt input1.txt

