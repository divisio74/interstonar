NAME = interstonar

SRC = interstonar.py \
      parser.py \
      local_mode.py \
      global_mode.py

all: $(NAME)

$(NAME):
	cp interstonar.py $(NAME)
	chmod +x $(NAME)

clean:
	rm -rf __pycache__
	rm -f *.pyc

fclean: clean
	rm -f $(NAME)

re: fclean all