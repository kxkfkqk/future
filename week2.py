def calculate(min,max):
    sum=0
    for i in range(min,(max+1)):
        sum+=i
    print(sum)
calculate(1,3)
calculate(4,8)
def avg(data):
    sum=0
    people=data["count"]
    for i in range(people):
        money=data["employees"][i]["salary"]
        sum+=money
    print(sum/people)
avg({
    "count":3,
    "employees":[
        {
                "name":"John",
                "salary":30000
        },
        {
                "name":"Bob",
                "salary":60000
        },
        {
                "name":"Jenny",
                "salary":50000
        }
        ]
})
def maxProduct(nums):
    anser=sorted(nums)
    print(anser[-1]*anser[-2])
maxProduct([5,20,2,6])
maxProduct([10,-20,0,3])

def twoSum(nums,target):
    z=0
    x=0
    anser=[]
    for i in nums:
        first=target-i
        x+=1
        if first in nums:
            x1=x-1
            anser+=[x1]
        else:
            continue 
    return anser       
result=twoSum([2,11,7,15],9)
print(result)

def maxZeros(nums):
    x=[]
    number=0
    for i in nums:
        if i==0:
            number+=1
        else:
            x+=[number]
            number=0
    x+=[number]
    print(max(x))
maxZeros([0,1,0,0])
maxZeros([1,0,0,0,0,1,0,1,0,0])
maxZeros([1,1,1,1,1])
