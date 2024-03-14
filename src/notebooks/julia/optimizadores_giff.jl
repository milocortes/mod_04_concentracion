using Plots
using Zygote
using LaTeXStrings


x1 = range(-5, stop=10, length=1000)
x2 = range(0, stop=15, length=1000)


function branin(x1,x2; a=1, b=5.1/(4π^2), c=5/π, r=6, s=10, t=1/(8π))
    return a*(x2-b*x1^2+c*x1-r)^2 + s*(1-t)*cos(x1) + s
end


### Steepest descent
steepest_results = []

rho = 0.01
n = 1000
x = 5
y = 15
z = branin(x,y)

push!(steepest_results, [x,y,z])
X = [x,y]

for it in 1:n 
    gt = collect(gradient(branin, x,y))
    X = X - rho.*gt
    x,y = X
    z = branin(x,y)
    push!(steepest_results, [x,y,z])
    println(X)
end

### Momentum
momentum = []
rho = 0.01
beta = 0.9
m = zeros(2)
x = 5
y = 15
z = branin(x,y)

push!(momentum, [x,y,z])

X = [x,y]

for it in 1:n 
    gt = collect(gradient(branin, x,y)) 
    m = beta.*m + gt
    X = X - rho.*m
    x,y = X
    z = branin(x,y)
    push!(momentum, [x,y,z])

    println(X)
end

### Momentum Nesterov
momentum_nesterov = []
rho = 0.01
beta = 0.9
m = zeros(2)
x = 5
y = 15
z = branin(x,y)

push!(momentum_nesterov, [x,y,z])

X = [x,y]

for it in 1:n 
    x,y = X + beta.*m
    gt = collect(gradient(branin, x,y)) 
    m = beta.*m - rho.*gt
    X = X + m
    x,y = X
    z = branin(x,y)
    push!(momentum_nesterov, [x,y,z])

    println(X)
end

### Adam
adam = []
rho = 0.9
beta_uno = 0.9
beta_dos = 0.999
epsilon = 10^-6
m = zeros(2)
s = zeros(2)

x = 5
y = 15
z = branin(x,y)

push!(adam, [x,y,z])

X = [x,y]

for it in 1:n 
    gt = collect(gradient(branin, x,y))
    m = beta_uno.*m + beta_uno*(1-beta_uno).*gt
    s = beta_dos.*s + beta_dos*(1-beta_dos).*gt.^2

    m_tilde = m./(1-(beta_uno^(it)))
    s_tilde = s./(1-(beta_dos^(it)))


    X = X - rho .* (m_tilde ./ (sqrt.(s_tilde) .+ epsilon))
    #(rho*(.√s_tilde .+ epsilon).^-1).*m_tilde
    
    x,y = X
    z = branin(x,y)
    push!(adam, [x,y,z])

    println(X)
end


#p_surface = surface(x1, x2, branin, alpha = 0.96, legend=:topleft, title = "Minimización de la función Branin", size=(1200,800),rev=true)

p_surface = surface(x1, x2, branin,  legend=:topleft, title = "Minimización de la función Branin", size=(1200,800),c=cgrad(:lisbon), display_option=Plots.GR.OPTION_SHADED_MESH)


scatter!(p_surface, [-pi], [12.275], [branin(-pi,12.275)], color = :black, label = "Minimo local 1", legend=:topleft, markersize=6)
scatter!(p_surface, [pi], [2.275], [branin(-pi,12.275)], color = :black, label = "Minimo local 2", legend=:topleft, markersize=6)
scatter!(p_surface, [9.42478], [2.475], [branin(9.42478,2.475)], color = :black, label = "Minimo local 3", legend=:topleft, markersize=6)

i = 1
scatter!(p_surface, [steepest_results[i][1]], [steepest_results[i][2]], [steepest_results[i][3]], color = :green, label = L"Steepest, $\rho=0.01$", legend=:topleft, markersize=6)
scatter!(p_surface, [momentum[i][1]], [momentum[i][2]], [momentum[i][3]], color = :red, label = L"Momentum, $\rho=0.01$, $\beta=0.9$", legend=:topleft, markersize=6)
scatter!(p_surface, [momentum_nesterov[i][1]], [momentum_nesterov[i][2]], [momentum_nesterov[i][3]], color = :blue, label = L"Momentum Nesterov, $\rho=0.01$, $\beta=0.9$", legend=:topleft, markersize=6)
scatter!(p_surface, [adam[i][1]], [adam[i][2]], [adam[i][3]], color = :orange, label = L"Adam, $\rho=0.9$,, $\beta_1=0.9$, $\beta_2=0.99$", legend=:topleft, markersize=6)


anim = @animate for i in 1:240
    println(i)
    p_surface_giff = deepcopy(p_surface)

    scatter!(p_surface_giff, [steepest_results[i][1]], [steepest_results[i][2]], [steepest_results[i][3]], color = :green, label = L"Steepest, $\rho=0.01$", legend=:topleft, primary=false, markersize=6)
    scatter!(p_surface_giff, [momentum[i][1]], [momentum[i][2]], [momentum[i][3]], color = :red, label = L"Momentum, $\rho=0.01$, $\beta=0.9$", legend=:topleft, primary=false, markersize=6)
    scatter!(p_surface_giff, [momentum_nesterov[i][1]], [momentum_nesterov[i][2]], [momentum_nesterov[i][3]], color = :blue, label = L"Momentum Nesterov, $\rho=0.01$, $\beta=0.9$", legend=:topleft, primary=false, markersize=6)
    scatter!(p_surface_giff, [adam[i][1]], [adam[i][2]], [adam[i][3]], color = :orange, label = L"Adam, $\rho=0.9$,, $\beta_1=0.9$, $\beta_2=0.99$", legend=:topleft, primary=false, markersize=6)

    scatter!(p_surface, [steepest_results[i][1]], [steepest_results[i][2]], [steepest_results[i][3]], color = :green, label = L"Steepest, $\rho=0.01$", legend=:topleft, primary=false, markersize=6)
    scatter!(p_surface, [momentum[i][1]], [momentum[i][2]], [momentum[i][3]], color = :red, label =  L"Momentum, $\rho=0.01$, $\beta=0.9$", legend=:topleft, primary=false, markersize=6)
    scatter!(p_surface, [momentum_nesterov[i][1]], [momentum_nesterov[i][2]], [momentum_nesterov[i][3]], color = :blue, label = L"Momentum Nesterov, $\rho=0.01$, $\beta=0.9$", legend=:topleft, primary=false, markersize=6)
    scatter!(p_surface, [adam[i][1]], [adam[i][2]], [adam[i][3]], color = :orange, label = L"Adam, $\rho=0.9$,, $\beta_1=0.9$, $\beta_2=0.99$", legend=:topleft, primary=false, markersize=6)
end
gif(anim, "optimizadores.gif")
