from functools import cmp_to_key

#A task instance
class TaskIns(object):

    def __init__(self, start, end, priority, name ,id):
        self.start    = start
        self.end      = end
        self.usage    = 0
        self.priority = priority
        self.name     = name.replace("\n", "")
        self.id = id

    #Allow an instance to use the cpu (periodic)
    def use(self, usage):
        self.usage += usage
        if self.usage >= self.end - self.start:
            return True
        return False

    def __repr__(self):
        return str(self.name) + "#" + str(self.id) + " - start: " + str(self.start) + " priority: " + str(self.priority)  

    def get_unique_name(self):
        return str(self.name) + "_P" + str(self.id)

#Task types (templates for periodic tasks)
class TaskType(object):

    def __init__(self, period, release, execution, deadline, name):
        self.period    = period
        self.release   = release
        self.execution = execution
        self.deadline  = deadline
        self.name      = name

#Priority comparison
def priority_cmp(one, other):
    if one.priority < other.priority:
        return -1
    elif one.priority > other.priority:
        return 1
    return 0

# read taskes file
def read_data_from_file(path):
    file = open(path)
    lines = file.readlines()
    
    tasks = []
    for line in lines:
        line = line.split(' ')
        for i in range (0,2):
            line[i] = float(line[i])*10

        if len(line) == 3:
            name = line[2]

        elif len(line) == 2:
            name = 'T'
        else:
            raise Exception('Invalid tasks.txt file structure')
        
        if int(line[1])>0:
            tasks.append(TaskType(period=line[1], release=0, execution=line[0], deadline=line[1], name=name))
    return  tasks 

if __name__ == '__main__':
    
    # time apperes in chart
    time_to_run = 10*28
    tasks =read_data_from_file('tasks.txt')

    tasks_instanses = []
    for task in tasks:
        cnt=1
        for i in range(0, time_to_run , 5):
            if  (i - task.release) % task.period == 0 and i >= task.release:
                start = i
                end = start + task.execution
                priority = start + task.deadline - task.execution
                tasks_instanses.append(TaskIns(start=start, end=end, priority=priority, name=task.name,id=cnt))
                cnt+=1

    #Html output start
    html_colors = { 'T1':'#FFFACD', 'T2':'#B6D3EF', 'T3':'#999999', 'Empty':'white', 'Finish':'green'}
    html = '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>LLF Scheduling</title>
            <style> p{ background-color :white ;}</style>
        </head>
        <body style="display: inline-block;width: 5000px;">'''

    #Simulate clock
    clock_step = 5
    for i in range(0, time_to_run, clock_step):
        #Fetch possible tasks that can use cpu and sort by priority
        possible = []
        for t in tasks_instanses:
            if t.start <= i:
                possible.append(t)
        possible = sorted(possible, key=cmp_to_key(priority_cmp))

        #Select task with highest priority
        if len(possible) > 0:
            on_cpu = possible[0]
            print (on_cpu.get_unique_name() , " uses the processor. " ),
            
            if i%10==0:
                html += '<div style="float: left; text-align: left; width: 1px; height: 50px; background-color: black;">' + '<br /><p></p></div>'
            
            html += '<div style="float: left; text-align: center; width: 50px; height: 50px; background-color:' + html_colors[on_cpu.name] + ';"> '+ on_cpu.get_unique_name() +'<br /><p>.........</p></div>'
            html += '<div style="float: left; text-align: left; width: 30px; height: 50px; background-color: '+html_colors[on_cpu.name]+';">' + '<br /><p>' + str((i+5)/10.0) + '</p></div>'
             
            on_cpu.priority += 1

            # check if task is ended 
            if on_cpu.use(clock_step):
                tasks_instanses.remove(on_cpu)
                html += '<div style="float: left; text-align: center; width: 3px; height: 50px; background-color:' + html_colors['Finish'] + ';"></div>'
                print ("Finish!") ,
        else:
            print ('No task uses the processor. ')
            html += '<div style="float: left; text-align: center; width: 50px; height: 50px; background-color:' + html_colors['Empty'] + ';">' + '<br /><p> -------- </p></div>'
            html += '<div style="float: left; text-align: left; width: 30px; height: 50px; background-color: '+html_colors['Empty']+';">' + '<br /><p>' + str((i+5)/10.0) + '</p></div>'
        print ("\n")
        
    #Html output end
    html += "</body></html>"
    output = open('schedule_chart.html', 'w')
    output.write(html)
    output.close()
