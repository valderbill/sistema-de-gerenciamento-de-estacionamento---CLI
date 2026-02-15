from datetime import datetime
from typing import Dict, Optional

class Veiculo:
    def __init__(self, placa: str, tipo: str, hora_entrada: datetime):
        self.placa = placa
        self.tipo = tipo
        self.hora_entrada = hora_entrada
        self.hora_saida: Optional[datetime] = None

class Estacionamento:
    def __init__(self):
        self.vagas_carros = 50
        self.vagas_motos = 20
        self.vagas_pcd = 10
        self.veiculos: Dict[str, Veiculo] = {}
        self.veiculos_saida: Dict[str, Veiculo] = {}  # Histórico de veículos que saíram
        self.ocupadas_carros = 0
        self.ocupadas_motos = 0
        self.ocupadas_pcd = 0

    def registrar_entrada(self, placa: str, tipo: str) -> bool:
        tipo = tipo.lower()
        if placa in self.veiculos and not self.veiculos[placa].hora_saida:
            print(f"❌ Veículo {placa} já está no estacionamento!")
            return False

        if tipo == "carro":
            if self.ocupadas_carros >= self.vagas_carros:
                print("❌ Sem vagas disponíveis para carros!")
                return False
            self.ocupadas_carros += 1
        elif tipo == "moto":
            if self.ocupadas_motos >= self.vagas_motos:
                print("❌ Sem vagas disponíveis para motos!")
                return False
            self.ocupadas_motos += 1
        elif tipo == "pcd":
            if self.ocupadas_pcd >= self.vagas_pcd:
                print("❌ Sem vagas disponíveis para PCD!")
                return False
            self.ocupadas_pcd += 1
        else:
            print("❌ Tipo inválido! Use: carro, moto ou pcd")
            return False

        veiculo = Veiculo(placa, tipo, datetime.now())
        self.veiculos[placa] = veiculo
        print(f"✅ {tipo.upper()} {placa} registrado às {veiculo.hora_entrada.strftime('%H:%M:%S')}")
        return True

    def registrar_saida(self, placa: str) -> bool:
        if placa not in self.veiculos:
            print(f"❌ Veículo {placa} não encontrado!")
            return False

        veiculo = self.veiculos[placa]
        if veiculo.hora_saida:
            print(f"❌ Veículo {placa} já saiu do estacionamento!")
            return False

        veiculo.hora_saida = datetime.now()
        tempo_permanencia = veiculo.hora_saida - veiculo.hora_entrada
        horas = tempo_permanencia.total_seconds() / 3600
        minutos = (tempo_permanencia.total_seconds() % 3600) / 60
        segundos = tempo_permanencia.total_seconds() % 60

        # Atualizar vagas
        if veiculo.tipo == "carro":
            self.ocupadas_carros -= 1
        elif veiculo.tipo == "moto":
            self.ocupadas_motos -= 1
        elif veiculo.tipo == "pcd":
            self.ocupadas_pcd -= 1

        # Mover para a lista de veículos que saíram
        self.veiculos_saida[placa] = veiculo
        del self.veiculos[placa]  # Remover da lista de veículos ativos

        print(f"\n✅ {veiculo.tipo.upper()} {placa} saiu às {veiculo.hora_saida.strftime('%H:%M:%S')}")
        print(f"⏱️  Tempo de permanência: {int(horas)}h {int(minutos)}min {int(segundos)}s")
        return True

    def exibir_status(self):
        print("\n" + "="*60)
        print("📊 STATUS DO ESTACIONAMENTO")
        print("="*60)
        
        print(f"\n🚗 CARROS:")
        print(f"   Ocupadas: {self.ocupadas_carros}/{self.vagas_carros}")
        print(f"   Disponíveis: {self.vagas_carros - self.ocupadas_carros}")
        
        print(f"\n🏍️  MOTOS:")
        print(f"   Ocupadas: {self.ocupadas_motos}/{self.vagas_motos}")
        print(f"   Disponíveis: {self.vagas_motos - self.ocupadas_motos}")
        
        print(f"\n♿ PCD:")
        print(f"   Ocupadas: {self.ocupadas_pcd}/{self.vagas_pcd}")
        print(f"   Disponíveis: {self.vagas_pcd - self.ocupadas_pcd}")
        
        total_ocupadas = self.ocupadas_carros + self.ocupadas_motos + self.ocupadas_pcd
        total_vagas = self.vagas_carros + self.vagas_motos + self.vagas_pcd
        print(f"\n📈 TOTAL: {total_ocupadas}/{total_vagas} vagas ocupadas")
        print("="*60)

    def listar_veiculos(self):
        veiculos_ativos = [v for v in self.veiculos.values() if not v.hora_saida]
        veiculos_saida = [v for v in self.veiculos_saida.values()]
        
        if not veiculos_ativos and not veiculos_saida:
            print("\n📭 Nenhum veículo no estacionamento")
            return
        
        print("\n" + "="*60)
        print("🚙 VEÍCULOS NO ESTACIONAMENTO")
        print("="*60)
        for veiculo in veiculos_ativos:
            print(f"{veiculo.tipo.upper():5} | {veiculo.placa:10} | Entrada: {veiculo.hora_entrada.strftime('%H:%M:%S')}")
        
        print("\n" + "="*60)
        print("🚗 VEÍCULOS QUE SAÍRAM")
        print("="*60)
        for veiculo in veiculos_saida:
            print(f"{veiculo.tipo.upper():5} | {veiculo.placa:10} | Entrada: {veiculo.hora_entrada.strftime('%H:%M:%S')} | Saída: {veiculo.hora_saida.strftime('%H:%M:%S')}")
        print("="*60)

def menu():
    estacionamento = Estacionamento()
    
    while True:
        print("\n" + "="*60)
        print("🅿️  SISTEMA DE ESTACIONAMENTO")
        print("="*60)
        print("1. Registrar Entrada")
        print("2. Registrar Saída")
        print("3. Exibir Status")
        print("4. Listar Veículos")
        print("5. Sair")
        print("="*60)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            placa = input("Placa do veículo: ").strip().upper()
            tipo = input("Tipo (carro/moto/pcd): ").strip().lower()
            estacionamento.registrar_entrada(placa, tipo)
        
        elif opcao == "2":
            placa = input("Placa do veículo: ").strip().upper()
            estacionamento.registrar_saida(placa)
        
        elif opcao == "3":
            estacionamento.exibir_status()
        
        elif opcao == "4":
            estacionamento.listar_veiculos()
        
        elif opcao == "5":
            print("\n👋 Encerrando sistema...")
            break
        
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    menu()
