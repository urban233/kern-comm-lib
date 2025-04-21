import kern_comm_lib as kern


if __name__ == '__main__':
  kern.init_kern_logging("example_logging")
  kern.LOG_INFO("This is an info message")
  kern.LOG_WARNING("This is an warning message")
  kern.LOG_ERROR("This is an error message")
  kern.LOG_FATAL("This is a fatal message")
