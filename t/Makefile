#VERBOSE = -v
VERBOSE =

all:
	
test : test-pre test-post

test-pre :
	prove $(VERBOSE) 01-add_category.sh
	prove $(VERBOSE) 02-add_alias.sh
	prove $(VERBOSE) 03-add_vip.sh
	prove $(VERBOSE) 04-add_filter.sh

test-main :
	prove $(VERBOSE) 10-toggle_rule.sh
	prove $(VERBOSE) 20-test_nc.sh

test-post :
	prove $(VERBOSE) 96-delete_filter.sh
	prove $(VERBOSE) 97-delete_vip.sh
	prove $(VERBOSE) 98-delete_alias.sh
	prove $(VERBOSE) 99-delete_category.sh

