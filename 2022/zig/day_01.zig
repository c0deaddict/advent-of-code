const std = @import("std");
const data = @embedFile("input/day_1.txt");
const split = std.mem.split;

pub fn main() !void {
    std.debug.print("{!d}\n", .{part1(data)});
    std.debug.print("{!d}\n", .{part2(data)});
}

pub fn totals(input: []const u8) ![]const i32 {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    var list = std.ArrayList(i32).init(allocator);
    defer list.deinit();

    var total: i32 = 0;
    var lines = split(u8, input, "\n");
    while (lines.next()) |line| {
        const trimmed_line = std.mem.trim(u8, line, " \r");
        if (trimmed_line.len == 0) {
            try list.append(total);
            total = 0;
        } else {
            const n = std.fmt.parseInt(i32, line, 10) catch 0;
            total += n;
        }
    }
    try list.append(total);

    var s = try list.toOwnedSlice();
    std.sort.insertion(i32, s, {}, std.sort.desc(i32));
    return s;
}

pub fn part1(input: []const u8) !i32 {
    return (try totals(input))[0];
}

pub fn part2(input: []const u8) !i32 {
    const s = try totals(input);
    return s[0] + s[1] + s[2];
}

const example1 =
    \\1000
    \\2000
    \\3000
    \\
    \\4000
    \\
    \\5000
    \\6000
    \\
    \\7000
    \\8000
    \\9000
    \\
    \\10000
;

test "part1" {
    const result = part1(example1);
    try std.testing.expectEqual(@as(i32, 24000), try result);
}

test "part2" {
    const result = part2(example1);
    try std.testing.expectEqual(@as(i32, 45000), try result);
}
