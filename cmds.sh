base_url="http://localhost:7755"
header_template="X-Principal: {\"user_id\":%d, \"student_id\":%d}"

# Function to construct the full header with dynamic values
function build_header() {
    # below re some positional args
    user_id=$1
    student_id=$2
    # Format the header template with provided IDs
    header=$(printf "$header_template" "$user_id" "$student_id")
    echo "$header"
}

# reading sys_args.
user_id=$1
student_id=$2

# running the func to generate the header for the subsequent reqs.
header=$(build_header "$user_id" "$student_id")

# # GET /student/assignments
curl -X GET -H "$header" "$base_url/student/assignments"

# GET /principal/teachers
# curl -H "$header" "$base_url/principal/teachers"
