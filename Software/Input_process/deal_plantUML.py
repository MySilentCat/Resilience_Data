# 解析plantUML文件，生成静态贝叶斯网络
# 时间：2023/10/24

import chardet

class Component_diagram_node:
    # 组件图节点
    def __init__(self, name):
        self.name = name #组件名称
        self.alias="" #组件别名
        self.parents = [] #父节点字典
        self.children = [] #子节点字典
        self.int=[] #组件连接的提供接口
          
class Component_diagram:
    #组件图
    def __init__(self,count) -> None:
        self.count=count
        self.names=[]
        self.adjacency_matrix=[[0 for i in range(count)] for i in range(count)]

        self.parents = {}
        self.children = {}
        # 创建一个名字与编号的字典，便于查找
        #index_list = [i for i in range(len(self.names))]
        self.variables_dict = {}

        self.interface = {}

    def set_index(self):
        index_list = [i for i in range(len(self.names))]
        self.variables_dict = dict(zip(self.names, index_list))
        print(self.variables_dict)

    # 构建父亲节点字典和子节点字典
    def build_parents_children(self):
        print('names: ',self.names)
        for i in range(self.count):
            temp1 = []
            temp2 = []
            for j in range(self.count):
                if self.adjacency_matrix[i][j] == 1:
                    temp1.append(self.names[j])# 子节点
                if self.adjacency_matrix[j][i] == 1:
                    temp2.append(self.names[j])# 父节点
            self.parents[self.names[i]] = temp1
            self.children[self.names[i]] = temp2
        print('children:', self.children)

    # 构建邻接矩阵
    def build_adjacency_matrix(self):
        self.count = len(self.names)
        adjacency_matrix = [[0 for i in range(self.count)] for i in range(self.count)]
        for i in range(self.count):
            for child in self.children[self.names[i]]:
                print(i,self.variables_dict[child])
                adjacency_matrix[i][self.variables_dict[child]] = 1
        self.adjacency_matrix = adjacency_matrix

def get_str_btw(s, f, b):
    par = s.partition(f)
    return (par[2].partition(b))[0][:]

def read_comp_uml(filename,main,sub):
    #print(filename)
    # 获取文件编码格式
    f = open(filename, 'rb')
    data = f.read()
    encoding = chardet.detect(data)['encoding']
    f.close()
    f=open(filename,'r',encoding=encoding)
    Component_list=[]
    Component_map={}
    
    with f:
        data=f.read()
        data_list=data.split("\n")
        #print(data_list)
        for i in range(len(data_list)):
            if '[' in data_list[i]:
                temp_Component=Component_diagram_node(get_str_btw(data_list[i], '[', ']'))
                temp_list=data_list[i].split(" ")
                for j in range(len(temp_list)):
                    if temp_list[j]=='as':
                        temp_Component.alias=temp_list[j+1]
                Component_list.append(temp_Component)
                Component_map[temp_Component.alias]=temp_Component
            else:
                if 'component' in data_list[i]:
                    temp_list=data_list[i].split(" ")
                    temp_Component=Component_diagram_node("")
                    for j in range(len(temp_list)):
                        if temp_list[j]=='component':
                            temp_Component.name=temp_list[j+1]
                        if temp_list[j]=='as':
                            temp_Component.alias=temp_list[j+1]
                    Component_list.append(temp_Component)
                    Component_map[temp_Component.alias]=temp_Component
            
            if '.>' in data_list[i] or '->' in data_list[i]:
                # 先按空格分割，再按箭头分割
                temp_list1=data_list[i].split(" ")
                temp_list = []
                for j in range(len(temp_list1)):
                    # 每个都按.>或->分割
                    if '.>' in data_list[i]:
                        temp_list.extend(temp_list1[j].split('.>'))
                    else:
                        temp_list.extend(temp_list1[j].split('->'))

                for p in Component_list:
                    temp_p=""
                    if '[' in temp_list[0]:
                        temp_p = get_str_btw(temp_list[0], '[', ']')
                    else:
                        temp_p=temp_list[0]
                    if p.name==temp_p or p.alias==temp_p:
                        for c in Component_list:
                            temp_c=""
                            if '[' in temp_list[-1]:
                                temp_c = get_str_btw(temp_list[-1], '[', ']')
                            else:
                                temp_c=temp_list[-1]
                            if c.name==temp_c or c.alias==temp_c:
                                if c not in p.children:
                                    p.children.append(c)
                                    c.parents.append(p)
            
            if '<.' in data_list[i] or '<-' in data_list[i]:
                temp_list1=data_list[i].split(" ")
                temp_list = []
                for j in range(len(temp_list1)):
                    # 每个都按.>或->分割
                    if '<.' in data_list[i]:
                        temp_list.extend(temp_list1[j].split('<.'))
                    else:
                        temp_list.extend(temp_list1[j].split('<-'))
                for p in Component_list:
                    temp_p=""
                    if '[' in temp_list[-1]:
                        temp_p = get_str_btw(temp_list[-1], '[', ']')
                    else:
                        temp_p=temp_list[-1]
                    if p.name==temp_p or p.alias==temp_p:
                        for c in Component_list:
                            temp_c=""
                            if '[' in temp_list[0]:
                                temp_c = get_str_btw(temp_list[0], '[', ']')
                            else:
                                temp_c=temp_list[0]
                            if c.name==temp_c or c.alias==temp_c:
                                if c not in p.children:   
                                    p.children.append(c)
                                    c.parents.append(p)
            
            if '-' in data_list[i] and '>' not in data_list[i] and '<' not in data_list[i] and ')' not in data_list[i] and '(' not in data_list[i]:
                temp_list1=data_list[i].split(" ")
                temp_list = []
                for j in range(len(temp_list1)):
                    # 每个都按-分割
                    temp_list.extend(temp_list1[j].split('-'))
                temp1=temp_list[0]
                temp2=temp_list[-1]
                for p in Component_list:
                    if temp1==p.name or temp1==p.alias:
                        p.int.append(temp2)
                    else:
                        if temp2==p.name or temp2==p.alias:
                           p.int.append(temp1)
            
        interface = {}
        
        for i in range(len(data_list)):
            if '-(' in data_list[i]:
                temp_list1=data_list[i].split(" ")
                temp_list = []
                for j in range(len(temp_list1)):
                    # 每个都按或-(分割
                    temp_list.extend(temp_list1[j].split('-('))
                #print(temp_list)
                temp1=temp_list[0]
                temp2=temp_list[-1]
                
                for p in Component_list:
                    if temp1==p.name or temp1==p.alias:
                        for c in Component_list:
                            if temp2 in c.int:
                                if c not in p.children:
                                    p.children.append(c)
                                    c.parents.append(p)
                                    #interface.append([p.alias,c.alias])
                                    if c.alias not in interface.keys():
                                        interface[c.alias] = [p.alias]
                                    else:
                                        interface[c.alias].append(p.alias)

            
            if ')-' in data_list[i]:
                temp_list1=data_list[i].split(" ")
                temp_list = []
                for j in range(len(temp_list1)):
                    # 每个都按或)-分割
                    temp_list.extend(temp_list1[j].split(')-'))
                temp1=temp_list[-1]
                temp2=temp_list[0]
                for p in Component_list:
                    if temp1==p.name or temp1==p.alias:
                        for c in Component_list:
                            if temp2 in c.int:
                                if c not in p.children:
                                    p.children.append(c)
                                    c.parents.append(p)
                                    if c.alias not in interface.keys():
                                        interface[c.alias] = [p.alias]
                                    else:
                                        interface[c.alias].append(p.alias)
        
        # print([node.name for node in Component_list])
                                        
        # for c in Component_list:
        #     print(c.name)
        #     print(c.alias)
        #     print('..........................................')
        #     for child in c.children:
        #         print(child.name)
        #         print(child.alias)
        #     print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        # raise ValueError
        component_diagram=Component_diagram(len(Component_list))
        #component_diagram.count=len(Component_list)
        count=0
        for component_node in Component_list:
            if ' ' in  component_node.name:
                if component_node.alias!="":
                    component_diagram.names.append(component_node.alias)
                else:
                    component_node.alias="component"+str(count)
                    component_diagram.names.append(component_node.alias)
                    count+=1
            else:
                for c in component_node.name:
                    if '\u4e00' <= c <= '\u9fa5':
                        if component_node.alias!="":
                            component_diagram.names.append(component_node.alias)
                            break
                        else:
                            component_node.alias="component"+str(count)
                            component_diagram.names.append(component_node.alias)
                            count+=1
                            break
                    else:
                        component_diagram.names.append(component_node.name)
                        break

        for i in range(len(Component_list)):
            for child in Component_list[i].children:
                for j in range(len(Component_list)):
                    if Component_list[j].name==child.name or Component_list[j].alias==child.alias:
                        component_diagram.adjacency_matrix[i][j]=1
        print(component_diagram.names)
        component_diagram.build_parents_children()
        print(component_diagram.children)
        component_diagram.set_index()
        component_diagram.build_adjacency_matrix()
        new_interface = {}
        print(interface)
        #raise ValueError
        for key,value in interface.items():
            new_key = key
            if key not in component_diagram.names:
                for comp in Component_list:
                    if comp.alias == key:
                        new_key = comp.name
            new_value = []
            for v in value:
                if v not in component_diagram.names:
                    for comp in Component_list:
                        if comp.alias == v:
                            new_value.append(comp.name)
                else:
                    new_value.append(v)
            new_interface[new_key] = new_value
        interface = new_interface.copy()
        print(interface)
        new_interface = {}
        for key,value in interface.items():
            for c in value:
                if c not in new_interface.keys():
                    new_interface[c] = [key]
                else:
                    new_interface[c].append(key)
        print(new_interface)
        #new_interface = interface
        #raise ValueError
        component_diagram.interface = new_interface

        
        #print(component_diagram.names)
        #raise ValueError
        return component_diagram, Component_list


def print_to_txt(component_diagram:Component_diagram,filename):
    f=open(filename,'w')
    with f:
        f.write(str(component_diagram.count))
        f.write("\n\n")
        temp_name_list=""
        for name in component_diagram.names:
            temp_name_list+=name+" "
        f.write(temp_name_list[0:len(temp_name_list)-1])
        f.write("\n\n")
        temp=""
        for num_list in component_diagram.adjacency_matrix:
            temp_num_list=""
            for num in num_list:
                temp_num_list+=str(num)+" "
            temp+=temp_num_list[0:len(temp_num_list)-1]
            temp+="\n"
        
        f.write(temp[0:len(temp)-1])
        
def comp_wsd_to_txt(file1,main,sub):
    component_diagram, Component_list = read_comp_uml(file1,main,sub)
    #component_diagram.set_index()
    return component_diagram

if __name__ == "__main__":
    #filename='E:/项目相关/华为软件架构安全/二期/界面/resilience_gui/models/ticket_booking_sys/compomenet_uml.wsd'
    #component_diagram = read_comp_uml(filename)
    #print_to_txt(component_diagram, 'E:/项目相关/华为软件架构安全/二期/界面/resilience_gui/models/ticket_booking_sys/123.txt')
    file1=r"E:\Graduation_Design_Docker\Input_process\网上商城系统.wsd"
    comp_wsd_to_txt(file1)