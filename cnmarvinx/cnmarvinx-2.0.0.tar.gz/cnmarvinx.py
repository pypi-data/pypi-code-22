''' This is my first python '''
def print_lol(the_list):
      '''定义递归函数'''
      for each_item in the_list:
            if isinstance(each_item, list):
                  print_lol(each_item)
            else:
                  print(each_item)
