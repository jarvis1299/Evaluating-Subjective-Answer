from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import pymysql
class Register:
    def __init__(self,root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("1920x1080+0+0")
        self.root.config(bg="white")
        #===Bg Image====

        self.bg = ImageTk.PhotoImage(file ="Images/p3.jpg")
        bg = Label(self.root,image=self.bg).place(x=250,y=0)

        #===LEFT IMAGE===
        self.left = ImageTk.PhotoImage(file ="Images/p5.jpg")
        left = Label(self.root,image=self.left).place(x=80,y=100,width=400,height=600)

        #====Register Frame====
        frame1 = Frame(self.root,bg="white")
        frame1.place(x=480,y=100,width=800,height=600)

        title=Label(frame1,text="REGISTER HERE",font=("times new roman",20,"bold"),bg="white",fg="green").place(x=300,y=30)

        #======= Row 1  
        f_name=Label(frame1,text="First Name",font=("times new roman",16,"bold"),bg="white",fg="gray").place(x=50,y=100)
        self.txt_fname = Entry(frame1,font=("times new roman",16),bg="lightgray")
        self.txt_fname.place(x=50,y=130,width=250)

        l_name=Label(frame1,text="Last Name",font=("times new roman",16,"bold"),bg="white",fg="gray").place(x=430,y=100)
        self.txt_lname = Entry(frame1,font=("times new roman",16),bg="lightgray")
        self.txt_lname.place(x=430,y=130,width=250)
        #======= Row 2
        contact=Label(frame1,text="Contact No.",font=("times new roman",16,"bold"),bg="white",fg="gray").place(x=50,y=180)
        self.txt_contact = Entry(frame1,font=("times new roman",16),bg="lightgray")
        self.txt_contact.place(x=50,y=210,width=250)

        email = Label(frame1,text="User ID",font=("times new roman",16,"bold"),bg="white",fg="gray").place(x=430,y=180)
        self.txt_email = Entry(frame1,font=("times new roman",16),bg="lightgray")
        self.txt_email.place(x=430,y=210,width=250)
        #======= Row 3
        question = Label(frame1,text="Security Question",font=("times new roman",16,"bold"),bg="white",fg="gray").place(x=50,y=260)
        self.cmb_quest= ttk.Combobox(frame1,font=("times new roman",13),state='readonly',justify=CENTER)
        self.cmb_quest['values']=("Select","Your First Pet Name","Your Birth Place","Your first Laptop")
        self.cmb_quest.place(x=50,y=290,width=250)
        self.cmb_quest.current(0)

        answer = Label(frame1,text="Answer",font=("times new roman",16,"bold"),bg="white",fg="gray").place(x=430,y=260)
        self.txt_answer = Entry(frame1,font=("times new roman",16),bg="lightgray")
        self.txt_answer.place(x=430,y=290,width=250)

        #======= Row 4
        password=Label(frame1,text="Password",font=("times new roman",16,"bold"),bg="white",fg="gray").place(x=50,y=340)
        self.txt_password = Entry(frame1,font=("times new roman",16),show="*",bg="lightgray")
        self.txt_password.place(x=50,y=370,width=250)

        cpassword = Label(frame1,text="Confirm Password",font=("times new roman",16,"bold"),bg="white",fg="gray").place(x=430,y=340)
        self.txt_cpassword = Entry(frame1,font=("times new roman",16),show="*",bg="lightgray")
        self.txt_cpassword.place(x=430,y=370,width=250)

        #====== terms
        self.var_chk=IntVar()
        chk= Checkbutton(frame1,text="I Agree the Terms & Conditions",variable=self.var_chk,onvalue=1,offvalue=0,bg="white",font=("times new roman",12)).place(x=50,y=420)

        btn_register = Button(frame1,text="Register Now",bg="red",cursor="hand2",command=self.register_data).place(x=50,y=470,width=100)

        btn_login = Button(self.root,text="Sign In",command=self.login_window,font=("times new roman",16),cursor="hand2").place(x=200,y=650,width=150)

    def login_window(self):
        self.root.destroy()
        import login 
              
    def clear(self):
        self.txt_fname.delete(0,END)
        self.txt_lname.delete(0,END)
        self.txt_contact.delete(0,END)
        self.txt_email.delete(0,END)
        self.cmb_quest.current(0)
        self.txt_answer.delete(0,END)
        self.txt_password.delete(0,END)
        self.txt_cpassword.delete(0,END)

    def register_data(self):
        if self.txt_fname.get()=="" or self.txt_contact.get()=="" or self.txt_email.get()=="" or  self.cmb_quest.get()=="Select" or self.txt_answer.get()=="" or self.txt_password.get()=="" or self.txt_cpassword.get()=="":
            messagebox.showerror("Error","All field Required",parent=self.root)
        elif self.txt_password.get()!=self.txt_cpassword.get():
            messagebox.showerror("Error","Password and Confirm Password should be same",parent=self.root)
        elif self.var_chk.get()==0:
            messagebox.showerror("Error","Please Agree our terms and conditions",parent=self.root)
        else:
            try:
                con=pymysql.connect(host="localhost",user="root",password="",database="student")
                cur=con.cursor()
                cur.execute("select * from studentdetails where email=%s",self.txt_email.get())
                row = cur.fetchone()
                #print(row)
                if row!=None:
                    messagebox.showerror("Error","User already Exist,Please try with another email",parent=self.root)
                else:
                    cur.execute("insert into studentdetails(f_name,l_name,contact,email,question,answer,password) values(%s,%s,%s,%s,%s,%s,%s)",
                            (self.txt_fname.get(),
                            self.txt_lname.get(),
                            self.txt_contact.get(),
                            self.txt_email.get(),
                            self.cmb_quest.get(),
                            self.txt_answer.get(),
                            self.txt_password.get()
                            ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Register Succesfull",parent=self.root)
                    self.clear()
            except Exception as es:
                messagebox.showerror("Error",f"Error due to: {str(es)}",parent=self.root)

     
root = Tk()
obj = Register(root)
root.mainloop() 
