

class Cat{
    int age;
    int birthday;
    
    Cat(int i, int j) {
        age = i;
        birthday = j;
    }
    
    Cat(int i) {
        this(i, i); 
    }
    
    Cat() {
        this(0); 
    }
}