from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import pymysql
import time
class login:
    def __init__(self,root):
        self.root = root 
        self.root.title("Login Window")
        self.root.geometry("1920x1080+0+0")

        #========= Background color=========
        left_lbl = Label(self.root,bg="#08A3D2",bd=0)
        left_lbl.place(x=0,y=0,relheight=1,width=700)

        right_lbl = Label(self.root,bg="#031F3C",bd=0)
        right_lbl.place(x=600,y=0,relheight=1,relwidth=1)
        #=========Login_Frames==========
        login_frame = Frame(self.root,bg="white")
        login_frame.place(x=400,y=100,width=900,height=600)

        self.nmims = ImageTk.PhotoImage(file ="Images/p1.png")
        nmims = Label(login_frame,image=self.nmims).place(x=450,y=50,width=256,height=109)

        email=Label(login_frame,text="User ID",font=("times new roman",20,"bold"),bg="white",fg="gray").place(x=450,y=170)
        self.txt_email=Entry(login_frame,font=("times new roman",15,"bold"),bg="lightgray")
        self.txt_email.place(x=450,y=220,width=350,height=35)

        pass_=Label(login_frame,text="Password",font=("times new roman",20,"bold"),bg="white",fg="gray").place(x=450,y=270)
        self.txt_pass_=Entry(login_frame,show="*",font=("times new roman",15,"bold"),bg="lightgray")
        self.txt_pass_.place(x=450,y=320,width=350,height=35)
        
        btn_reg = Button(login_frame,text="Register new account ?",command=self.register_window,font=("times new roman",14),bg="white",bd=0,fg="#B00857",cursor="hand2").place(x=445,y=370)
        btn_forget = Button(login_frame,text="Forget Password ?",command=self.forget_password_window,font=("times new roman",14),bg="white",bd=0,fg="red",cursor="hand2").place(x=640,y=370)

        btn_login = Button(login_frame,text="Login",command=self.login,font=("times new roman",20,"bold"),fg="white",bg="#B00857",cursor="hand2").place(x=445,y=440,width=150,height=40)


        #=========slider_frame==========
        
        self.image1 = ImageTk.PhotoImage(file ="Images/c1.jpg")
        self.image2 = ImageTk.PhotoImage(file ="Images/c2.jpg")

        Frame_slider = Frame(self.root)
        Frame_slider.place(x=50,y=180,width=650,height=433)

        self.lbl1 = Label(Frame_slider,image=self.image1,bd=0)
        self.lbl1.place(x=0,y=0)

        self.lbl2 = Label(Frame_slider,image=self.image2,bd=0)
        self.lbl2.place(x=650,y=0)
        self.x=650
        self.slider_function()

    def slider_function(self):
        self.x-=1
        if self.x==0:
            self.x=650
            time.sleep(1)
            #===== swaapp======
            self.new_img= self.image1
            self.image1 = self.image2
            self.image2 = self.new_img
            self.lbl1.config(image = self.image1)
            self.lbl2.config(image = self.image2)
        self.lbl2.place(x=self.x,y=0)
        self.lbl2.after(8,self.slider_function)

    def reset(self):
        self.cmb_quest.current(0)
        self.txt_new_password.delete(0,END)
        self.txt_answer.delete(0,END)
        self.txt_pass_.delete(0,END)
        self.txt_email.delete(0,END) 

    def forget_password(self):
        if self.cmb_quest.get()=="Select" or self.txt_answer.get()=="" or self.txt_new_password.get=="":
            messagebox.showerror("Error","All fields are required",parent=self.root2)
        else:
            try:
                con = pymysql.connect(host="localhost",user="root",password="",database="student")
                cur = con.cursor()
                cur.execute("select * from studentdetails where email=%s and question=%s and answer=%s",(self.txt_email.get(),self.cmb_quest.get(),self.txt_answer.get()))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please select the correct Security Question / Enter Answer",parent=self.root2 )
                else:
                    cur.execute("update studentdetails set password=%s where email=%s ",(self.txt_new_password.get(),   self.txt_email.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Your Password has been updates , Please login with new passwords",parent=self.root2)
                    self.reset()
                    self.root2.destroy()
            except Exception as es:
                messagebox.showerror("Error",f"Error Dur to: {str(es)}",parent=self.root) 



    def forget_password_window(self):
        if self.txt_email.get()=="":
            messagebox.showerror("Error","Please enter the email to reset your password",parent=self.root)
        else:
            try:
                con = pymysql.connect(host="localhost",user="root",password="",database="student")
                cur = con.cursor()
                cur.execute("select * from studentdetails where email=%s",self.txt_email.get())
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please enter the valid email to reset your password",parent=self.root )
                else:
                    con.close() 
                    self.root2 = Toplevel()
                    self.root2.title("Forget Password")
                    self.root2.geometry("400x400+500+200")
                    self.root2.configure(bg="white")
                    self.root2.focus_force()
                    self.root2.grab_set()

                    t = Label(self.root2,text="Forget Password",font=("times new roman",20,"bold"),bg="white",fg="red").place(x=0,y=10,relwidth=1)

                    #=====Forget Password=====
                    question = Label(self.root2,text="Security Question",font=("times new roman",16,"bold"),bg="white",fg="gray").place(x=50,y=100)
                    self.cmb_quest= ttk.Combobox(self.root2,font=("times new roman",13),state='readonly',justify=CENTER)
                    self.cmb_quest['values']=("Select","Your First Pet Name","Your Birth Place","Your first Laptop")
                    self.cmb_quest.place(x=50,y=130,width=250)
                    self.cmb_quest.current(0)

                    answer = Label(self.root2,text="Answer",font=("times new roman",16,"bold"),bg="white",fg="gray").place(x=50,y=180)
                    self.txt_answer = Entry(self.root2,font=("times new roman",16),bg="lightgray")
                    self.txt_answer.place(x=50,y=210,width=250)

                    new_password = Label(self.root2,text="New Password",font=("times new roman",16,"bold"),bg="white",fg="gray").place(x=50,y=260)
                    self.txt_new_password = Entry(self.root2,font=("times new roman",16),show="*",bg="lightgray")
                    self.txt_new_password.place(x=50,y=290,width=250)

                    btn_change_password = Button(self.root2,text="Reset Password",command=self.forget_password,bg="green",fg="white",font=("times new roman",15,"bold")).place(x=80,y=340)
                            
                

            except Exception as es:
                messagebox.showerror("Error",f"Error Dur to: {str(es)}",parent=self.root) 

    def register_window(self):
        self.root.destroy()
        import registration

    def login(self):
        if self.txt_email.get()=="" or self.txt_pass_.get()=="": 
            messagebox.showerror("Error","All fields are required",parent=self.root) 
        else:
            try:
                con = pymysql.connect(host="localhost",user="root",password="",database="student")
                cur = con.cursor()
                cur.execute("select * from studentdetails where email=%s and password=%s",(self.txt_email.get(),self.txt_pass_.get()))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Username and Password",parent=self.root)
                else:
                    self.root.destroy()
                    import sampleproject
                con.close()

            except Exception as es:
                messagebox.showerror("Error",f"Error Dur to: {str(es)}",parent=self.root) 

root = Tk()
obj = login(root)
root.mainloop() 