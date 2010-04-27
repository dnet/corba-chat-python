chat: chat.idl
	omniidl -bpython chat.idl

clean:
	rm -rf *.pyc chat/ chat__POA/ chat_idl.py

.PHONY: all clean
