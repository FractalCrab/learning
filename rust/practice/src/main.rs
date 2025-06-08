use std::fmt;


struct User{
    active:bool,
    username: String,
    email: String,
    sign_in_count: u64,
}

impl fmt::Debug for User{
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        // You can check flags on `f` (e.g., alternate for `{:#?}`)
        if f.alternate() {
            write!(f, "User {{\n active: {},\n  username: {}\n  email: {},\n  sign_in_count: {},\n }}", self.active, self.username, self.email, self.sign_in_count)
        } else {
            write!(f, "User {{\n active: {},\n  username: {}\n  email: {},\n  sign_in_count: {},\n }}", self.active, self.username, self.email, self.sign_in_count)
        }
    }
}


fn main() {
    let user1 = User{
        active: true,
        username: String::from("some@user.com"),
        email:String::from("some@user.com"),
        sign_in_count : 1,
        };

    println!("{:?}", user1);
   
}
