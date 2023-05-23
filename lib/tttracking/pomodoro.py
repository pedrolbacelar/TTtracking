from .helper import Helper
from time import sleep


class Pomodoro:
    def __init__(self, pomodoro_time, break_time, maxtime):
        self.helper = Helper()
        self.pomodoro_time = pomodoro_time * 60
        self.break_time = break_time * 60
        self.maxtime = maxtime * 60
        self.accumulated_time = 0
        self.last_time = self.helper.get_time_now()[1]
        self.rest_time = 60*(2.5)
        
    def run(self):
        """
        Pomodoro Function.
        It beeps an alarm after the pomodoro_time. The user needs to press enter to
        stop the alarm and continue to the break. The pomodoro also sets a soft alarm 
        after the break, the user also needs to press enter. Finally, if the cummulative time
        is higher than the maxtime, it plays a strong a alarm. The User can always when
        a alarm sounds add a number to represents the extra time asking for that task.
        """
        try:
            #--- Input flag
            flag_break = False

            while True:
                flag_input = False
                #--- Updates the cumulative time
                self.accumulated_time = self.helper.get_time_now()[1] - self.last_time

                #----- PRINTING -----
                if self.accumulated_time % 60 == 0:
                    sleep(1)
                    print(f"pomodoro >>> {round(self.accumulated_time/60)} minutes")

                #--- Check if the accumulated time is higher than the max time
                if self.accumulated_time > self.maxtime:
                    print(f"self.accumulated_time {self.accumulated_time}")
                    self.helper.printer(f"[WARNING] You have reached the maximum time of {self.maxtime} minutes ')", time= True, color= 'yellow')
                    self.helper.play('sirene')
                    while not flag_input:
                        feedback = input("\033[33mpomodoro >>> \033[0m")
                        if feedback == '':
                            flag_input = True
                            self.accumulated_time = 0
                            self.last_time = self.helper.get_time_now()[1]
                        
                        elif feedback.isnumeric():
                            self.maxtime = self.maxtime + int(feedback)
                            flag_input = True
                        else:
                            self.helper.printer(f"[ERROR] The input '{feedback}' is not valid. Please try again.", time= True, color= 'red')
                
                elif self.accumulated_time > self.break_time and flag_break:
                    print(f"self.accumulated_time {self.accumulated_time}")
                    self.helper.printer(f"[WARNING] You have reached the break time of {self.break_time} minutes ')", time= True, color= 'yellow')
                    self.helper.play('tick')
                    while not flag_input:
                        feedback = input("\033[33mbreak >>> \033[0m")
                        if feedback == '':
                            flag_input = True
                            self.accumulated_time = 0
                            self.last_time = self.helper.get_time_now()[1]
                            flag_break = False
                        
                        elif feedback.isnumeric():
                            self.break_time = self.break_time + int(feedback)
                            flag_input = True
                        else:
                            self.helper.printer(f"[ERROR] The input '{feedback}' is not valid. Please try again.", time= True, color= 'red')

                elif self.accumulated_time > self.pomodoro_time:
                    print(f"self.accumulated_time {self.accumulated_time}")
                    self.helper.printer(f"[WARNING] You have reached the pomodoro time of {self.pomodoro_time} minutes ')", time= True, color= 'yellow')
                    self.helper.play('clock')
                    while not flag_input:
                        feedback = input("\033[33mpomodoro >>> \033[0m")
                        if feedback == '':
                            flag_input = True
                            flag_break = True
                            self.accumulated_time = 0
                            self.last_time = self.helper.get_time_now()[1]
                            print("Time for a break")
                        
                        elif feedback.isnumeric():
                            self.pomodoro_time = self.pomodoro_time + int(feedback)
                            flag_input = True
                        else:
                            self.helper.printer(f"[ERROR] The input '{feedback}' is not valid. Please try again.", time= True, color= 'red')

                sleep(self.rest_time)
                
        except KeyboardInterrupt:
            return "task"

