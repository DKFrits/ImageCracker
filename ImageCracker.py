import subprocess
import sys, getopt

def main(argv):
	imagefile = ''
	wordlist = ''
	opts, args = getopt.getopt(argv, "f:w:", ["file=", "wordlist="])
	for opt, arg in opts:
		if opt in ("-f", "--file"):
			imagefile = arg
		elif opt in ("-w", "--wordlist"):
			wordlist = arg

	if imagefile == '' or wordlist == '':
		print('Usage: ImageCracker.py -f <file> -w <wordlist>')
		sys.exit()

	try:
		file = open(str(wordlist), 'r')
	except:
		print('Could not find file: {}'.format(wordlist))
		sys.exit(2)

	try:
		open(str(imagefile), 'r')
	except:
		print('Could not find file: {}'.format(imagefile))
		sys.exit(2)

	print('Starting bruteforce attack...\n')

	while True:
		line = file.readline()
		password = line.strip()

		cmd = ['steghide', 'info', str(imagefile), '-p', password]
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		o, e = proc.communicate()

		if not line:
			print('Could not find password in the given wordlist...')
			break

		if e.decode('ascii') != 'steghide: could not extract any data with that passphrase!\n':
			print('Output: ' + o.decode('ascii'))
			print('Found password: {}'.format(password))
			break

	file.close()

if __name__ == '__main__':
	main(sys.argv[1:])
