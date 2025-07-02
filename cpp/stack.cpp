#include <iostream>
#include <vector>

using namespace std;

class Stack{
    private:
      int size = 100;                    // declare the size of the vector
      vector<int> myvector; 
      int top = -1;
    public:
        Stack() : myvector(size, 0) {}
        void append(int element)
        {
           if (top>=99){
                cout<< "Stack overflow" << endl;
                return;
            } 
            myvector[++top] = element;
            cout << "Pushed " << element << " to stack\n";
        }
        int pop(){
             if (top<0){
                cout<< "Stack underflow" << endl;
                return -1;
            }
            return myvector[top--];
        }
          
        
};

int main(){
      Stack s;

      s.append(10);
      s.append(30);

       

}
  


