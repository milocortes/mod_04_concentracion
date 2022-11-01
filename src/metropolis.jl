using Random, Distributions,Plots,StatsPlots

Random.seed!(123)

let
σ2 = 1 ; τ2=10; μ=5
y =[9.37,10.18,9.16,11.60,10.33]
θ=0; δ2 =2; S = 100000
theta = []

for s in 1:S

    θ_star = rand(Normal(θ,sqrt(δ2)),1)[1]
    verosimilitud = sum(logpdf.(Normal(θ_star,sqrt(σ2)), y) .+ logpdf.(Normal(μ,sqrt(τ2)), θ_star))
    inicial = sum(logpdf.(Normal(θ,sqrt(σ2)), y) .+ logpdf.(Normal(μ,sqrt(τ2)), θ))

    log_r= verosimilitud - inicial
    if log(rand(Uniform(0, 1),1)[1]) < log_r
        θ = θ_star
    end

    push!(theta,θ)
end
plot(1:S, theta)
png("iteracion.png")
density(theta)
png("densidad.png")
end
